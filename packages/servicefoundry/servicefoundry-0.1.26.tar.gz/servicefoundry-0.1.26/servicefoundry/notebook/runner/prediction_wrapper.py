from .runtime_loader import import_runtime_module
from .service_wrapper import ServiceWrapper


class PredictionWrapper:
    def __init__(self, predict_script_str):
        self.predict_script_str = predict_script_str
        self.module = import_runtime_module("predict", predict_script_str)

    def predict(self, **kwargs):
        return self.module.predict(**kwargs)

    def create_service(self, parameters):
        return ServiceWrapper(self.predict_script_str, parameters)
