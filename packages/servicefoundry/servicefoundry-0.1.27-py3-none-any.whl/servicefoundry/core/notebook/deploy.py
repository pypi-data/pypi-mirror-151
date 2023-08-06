from IPython.core.display import display
from ipywidgets import Output, widgets

from servicefoundry.core.deploy import _deploy_local
from servicefoundry.core.notebook.notebook_callback import NotebookOutputCallBack

thread = None


def deploy_local(project_folder=""):
    global thread
    output = Output(
        layout=widgets.Layout(width="100%", height="auto", border="1px solid black")
    )
    if thread is not None and thread.is_alive():
        output.append_stdout("Stopping the old process.")
        thread.stop()
        thread.join()

    output_callback = NotebookOutputCallBack(output)
    thread = _deploy_local(project_folder, output_callback)

    box = widgets.Box(
        children=[output], layout=widgets.Layout(width="100%", height="auto")
    )
    display(box)
