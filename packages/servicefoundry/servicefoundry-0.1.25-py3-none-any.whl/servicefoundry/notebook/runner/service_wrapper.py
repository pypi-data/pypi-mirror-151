import os

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.const import BUILD_DIR
from servicefoundry.build.template.dummy_input_hook import DummyInputHook
from servicefoundry.build.template.sf_template import SfTemplate
from servicefoundry.build.template.template_workflow import TemplateWorkflow

TEMPLATE = "fastapi-inference"


class ServiceWrapper:
    def __init__(self, predict_script_str, parameters):
        self.project_folder = f"{BUILD_DIR}/service"
        tfs_client = ServiceFoundryServiceClient.get_client()
        sf_template = SfTemplate.get_template(f"truefoundry.com/v1/{TEMPLATE}")
        self.template_workflow = TemplateWorkflow(
            sf_template, DummyInputHook(tfs_client, parameters)
        )
        self.template_workflow.process_parameter(parameters=parameters)
        self.template_workflow.template.add_overwrite("predict.py", predict_script_str)

    def extra_files(self):
        return self.template_workflow.template.list_dir_and_files()

    def write(self, overwrite=False, verbose=True):
        self.template_workflow.write(
            out_folder="", overwrite=overwrite, verbose=verbose
        )

    def project_dir(self):
        return os.getcwd()
