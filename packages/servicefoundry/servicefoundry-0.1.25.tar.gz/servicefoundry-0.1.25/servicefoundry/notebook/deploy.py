from threading import Thread

from IPython.core.display import display
from ipywidgets import Output, widgets

from servicefoundry.build.build import LOCAL, REMOTE, build_and_deploy
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.notebook.notebook_callback import NotebookOutputCallBack

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

    deployment_thread = build_and_deploy(
        base_dir=project_folder,
        build=LOCAL,
        callback=NotebookOutputCallBack(output),
    )
    if isinstance(deployment_thread, Thread):
        thread = deployment_thread

    box = widgets.Box(
        children=[output], layout=widgets.Layout(width="100%", height="auto")
    )
    display(box)


def deploy(project_folder=""):
    deployment = build_and_deploy(base_dir=project_folder, build=REMOTE)
    print(deployment)
    # tail logs
    tfs_client = ServiceFoundryServiceClient.get_client()
    tfs_client.tail_logs(deployment["runId"], wait=True)
