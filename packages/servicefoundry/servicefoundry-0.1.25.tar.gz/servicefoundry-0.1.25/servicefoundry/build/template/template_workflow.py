from .template_parameters import STRING, NUMBER, OPTIONS, WORKSPACE

from .input_hook import InputHook
from .sf_template import SfTemplate


class TemplateWorkflow:
    def __init__(self, template: SfTemplate, input_hook: InputHook):
        self.template = template
        self.input_hook = input_hook
        self.parameters = None

    def process_parameter(self, parameters={}):
        final_params = {}
        for param in self.template.parameters:
            id = param.id
            if id in parameters:
                final_params[id] = parameters[id]
            elif param.kind == STRING:
                final_params[id] = self.input_hook.ask_string(param)
            elif param.kind == NUMBER:
                final_params[id] = self.input_hook.ask_number(param)
            elif param.kind == OPTIONS:
                final_params[id] = self.input_hook.ask_option(param)
            elif param.kind == WORKSPACE:
                final_params[id] = self.input_hook.ask_workspace(param)
        self.parameters = final_params

    def write(self, out_folder=None, overwrite=False, verbose=False):
        if out_folder is None:
            # Create new folder to hold template and rendered values.
            out_folder = self.parameters.get(
                "service_name", f"{self.template.template_id}_service"
            )
            print(f"Setting output folder to {out_folder}")
        self.template.write(
            self.parameters, out_folder, overwrite=overwrite, verbose=verbose
        )
