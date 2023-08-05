from pathlib import Path

from IPython.core.magic import register_cell_magic

from servicefoundry.build.util import read_text_from_file

from .prediction_wrapper import PredictionWrapper


class NotebookSession:
    def __init__(self):
        self.predict = None

    def set_predict(self, text):
        self.predict = PredictionWrapper(text)

    def get_predict(self):
        return self.predict


try:
    session
except NameError:
    session = NotebookSession()

get_predict = session.get_predict


def load_predict(file_name):
    path = Path(file_name)
    if not path.exists():
        raise RuntimeError(f"{file_name} not exist.")
    text = read_text_from_file(file_name)
    return PredictionWrapper(text)


def create_service(file_name, parameters):
    predictor = load_predict(file_name)
    return predictor.create_service(parameters)


@register_cell_magic
def sfy_load_predict(line, cell):
    global session
    try:
        session.set_predict(cell)
        print("Predict script loaded successfully.")
        print("Run servicefoundry.notebook.get_predict() to get the runner.")
    except ModuleNotFoundError as err:
        msg = f"Failed to register predict script. Caused by: {err}"
        print(msg)
        raise err
    return
