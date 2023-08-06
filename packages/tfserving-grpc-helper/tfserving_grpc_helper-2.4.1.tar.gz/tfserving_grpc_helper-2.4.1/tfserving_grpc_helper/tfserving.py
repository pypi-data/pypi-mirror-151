import threading
import numpy as np
import grpc
import tensorflow as tf
import math
import sys
import time

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc


class ResultCollect(object):
    def __init__(self, num_tests, concurrency):
        self._num_tests = num_tests
        self._concurrency = concurrency
        self._done = 0
        self._active = 0
        self._error = [None for _ in range(num_tests)]
        self._result = [None for _ in range(num_tests)]
        self._condition = threading.Condition()

    def add_result(self, response, index):
        with self._condition:
            self._result[index] = response

    def add_error(self, exception, index):
        with self._condition:
            self._error[index] = exception

    def inc_done(self):
        with self._condition:
            self._done += 1
            self._condition.notify()

    def dec_active(self):
        with self._condition:
            self._active -= 1
            self._condition.notify()

    def get_result(self):
        with self._condition:
            while self._done != self._num_tests:
                self._condition.wait()
            return self._result

    def get_error(self):
        with self._condition:
            while self._done != self._num_tests:
                self._condition.wait()
            return self._error

    def throttle(self):
        with self._condition:
            while self._active == self._concurrency:
                self._condition.wait()
            self._active += 1



class TFServingPredict(object):
    def __init__(
            self, 
            hostport, model_spec_name, model_spec_signature_name, 
            input_signatures, output_signatures, model_version=1,
            concurrency=1, time_out=60,
            max_retries=5, retry_delay=0.1,
        ):

        channel = grpc.insecure_channel(hostport, options=[
            ('grpc.max_send_message_length', 256 * 1024 * 1024),
            ('grpc.max_receive_message_length', 256 * 1024 * 1024),
        ])
        
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

        self.concurrency = concurrency

        self.input_signatures = input_signatures
        self.output_signatures = output_signatures

        self.model_spec_name = model_spec_name
        self.model_spec_signature_name = model_spec_signature_name
        self.model_version = int(model_version)

        self.time_out = time_out

        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def predict(self, X, batch_size):
        assert len(self.input_signatures) == len(X)

        data_size = len(X[list(self.input_signatures)[0]])
        batch_count = math.ceil(data_size / batch_size)

        idx_ranges = [(i * batch_size, ((i + 1) * batch_size) if i < batch_count - 1 else data_size) for i in
                      range(batch_count)]

        result_counter = ResultCollect(
            batch_count, concurrency=self.concurrency)


        def predict(idx, request, allow_retries, retry_delay):
            def _callback(result_future):
                """Callback function.

                Calculates the statistics for the prediction result.

                Args:
                result_future: Result future of the RPC.
                """
                exception = result_future.exception()
                if exception:
                    print("allow_retries: %d" % allow_retries)
                    print(exception)
                    sys.stdout.flush()

                    if allow_retries > 0:
                        time.sleep(retry_delay)
                        predict(idx, request, allow_retries-1, retry_delay)
                        # 终止本次请求
                        return
                    else:
                        result_counter.add_error(exception, idx)
                else:
                    response = {k: tf.make_ndarray(
                        result_future.result().outputs[k]) for k in self.output_signatures}
                    result_counter.add_result(response, idx)

                result_counter.inc_done()
                result_counter.dec_active()

            # 预测

            result_future = self.stub.Predict.future(request, self.time_out)
            result_future.add_done_callback(_callback)



        for idx, item in enumerate(idx_ranges):
            start, end = item
            request = predict_pb2.PredictRequest()
            request.model_spec.name = self.model_spec_name
            request.model_spec.version.value = self.model_version
            request.model_spec.signature_name = self.model_spec_signature_name

            for k in self.input_signatures:
                request.inputs[k].CopyFrom(
                    tf.make_tensor_proto(X[k][start:end]))

            result_counter.throttle()
            predict(idx, request, self.max_retries, self.retry_delay)

        r = result_counter.get_result()

        # 检查错误
        for e in result_counter.get_error():
            if e is not None:
                raise e

        for k in self.output_signatures:
            for r_item in r:
                if r_item is None:
                    raise "predict result is None"

        R = {k: np.concatenate([r_item[k] for r_item in r], axis=0) for k in self.output_signatures}

        return R
