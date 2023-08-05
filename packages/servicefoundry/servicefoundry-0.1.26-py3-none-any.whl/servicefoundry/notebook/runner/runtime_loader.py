import importlib.abc
import importlib.util


class RuntimeLoader(importlib.abc.SourceLoader):
    def __init__(self, data):
        self.data = data

    def get_source(self, fullname):
        return self.data

    def get_source(self, fullname):
        return self.data

    def get_data(self, path):
        return self.data.encode("utf-8")

    def get_filename(self, fullname):
        return "sfy://" + fullname + ".py"


def import_runtime_module(module_name, data):
    loader = RuntimeLoader(data)
    spec = importlib.util.spec_from_loader(module_name, loader, origin="built-in")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
