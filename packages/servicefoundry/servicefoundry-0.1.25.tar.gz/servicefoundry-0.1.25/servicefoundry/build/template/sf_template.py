import re
from os.path import join
from pathlib import Path

import yaml
import shutil
from jsonschema.exceptions import ValidationError
from mako.template import Template

from .generated_definition import GeneratedDefinition
from .sf_definition import SFDefinition
from .template_parameters import get_template_parameter
from .util import (
    get_or_create_template_folder,
    load_yaml_from_file,
    validate_schema,
    list_dir_and_files,
    check_conflict,
)
from ..const import TEMPLATE_DEF_FILE_NAME, SERVICE_DEF_FILE_NAME
from ..exceptions import ConfigurationException
from ..util import create_file_from_content

SPEC = "spec"
OVERWRITES = "overwrites"


class Parameters(dict):
    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)
        self.__dict__ = self


def render(value, parameters):
    try:
        template = Template(value)
        return template.render(parameters=parameters)
    except AttributeError as e:
        raise ConfigurationException(f"Failed to parse {value}. Caused by: {e}")


class SfTemplate:
    def __init__(self, template_id, template_folder, template):
        self.template_id = template_id
        self.template_folder = template_folder
        try:
            validate_schema(template, "schema/template_schema.json")
        except ValidationError as err:
            raise ConfigurationException(f"Template validation failed. {err.message}")

        spec = template[SPEC]
        self.base_build = spec["baseBuild"]
        self.base_component = spec["baseComponent"]
        self.post_init_instruction = spec["postInitInstruction"]
        self.overwrite = spec[OVERWRITES]
        self.parameters = [
            get_template_parameter(parameter) for parameter in spec["parameters"]
        ]
        self.comments: str = spec["comments"]
        self.overwrite_file = {}

    def add_overwrite(self, file_name, content):
        self.overwrite_file[file_name] = content

    def generate_service_def(self, sf_definition: SFDefinition):
        parameters = Parameters(sf_definition.parameters)
        base_build_id = self.base_build
        base_component_id = self.base_component
        resolved_overrides = self._resolve_variables(self.overwrite, parameters)
        if sf_definition.overwrites:
            resolved_overrides.extend(
                self._resolve_variables(sf_definition.overwrites, parameters)
            )

        definition = GeneratedDefinition(
            base_build_id, base_component_id, resolved_overrides
        )
        return definition

    def list_dir_and_files(self):
        dirs, files = list_dir_and_files(self.template_folder)
        files.remove(TEMPLATE_DEF_FILE_NAME)
        files.append(SERVICE_DEF_FILE_NAME)
        return dirs, files

    def write_parameter_file(self, out_folder, parameters):
        # Write parameters into servicefoundry.yaml
        with open(join(out_folder, SERVICE_DEF_FILE_NAME), "w") as template_file:
            yaml.dump(
                {
                    "template": f"truefoundry.com/v1/{self.template_id}",
                    "parameters": parameters,
                },
                template_file,
                sort_keys=False,
            )
            template_file.write("overwrites:\n")
            for line in self.comments.splitlines():
                template_file.write(f"#  {line}\n")

    def write(self, parameters, out_folder, overwrite=False, verbose=False):
        Path(out_folder).mkdir(parents=True, exist_ok=True)
        dirs, files = self.list_dir_and_files()
        for _dir in dirs:
            Path(join(out_folder, _dir)).mkdir(parents=True, exist_ok=True)
        conflicting_files = check_conflict(out_folder, files)
        conflicting_files_str = ", ".join(conflicting_files)
        if not overwrite and len(conflicting_files) > 0:
            raise ConfigurationException(
                f"Can't write project. "
                f"Files already exist [{conflicting_files_str}]. "
                + f"Use overwrite flag to overwrite file."
            )
        elif len(conflicting_files) > 0:
            print(f"Going to overwrite files [{conflicting_files_str}]")

        for file in files:
            if file == SERVICE_DEF_FILE_NAME:
                self.write_parameter_file(out_folder, parameters)
            elif file in self.overwrite_file:
                print(f"File replaced: {file} (user provided)")
                create_file_from_content(
                    join(out_folder, file), self.overwrite_file[file]
                )
            else:
                shutil.copy2(join(self.template_folder, file), join(out_folder, file))
            if verbose:
                print(f"File created: {file}")

    def _resolve_variables(self, overwrite_dict, parameters):
        resolved_values = []
        for overwrite_key, overwrite_value in overwrite_dict.items():
            resolved_values.append(
                (
                    overwrite_key,
                    self._resolve_variable(overwrite_key, overwrite_value, parameters),
                )
            )
        return resolved_values

    def _resolve_variable(self, key, value, parameters):
        if isinstance(value, dict):
            ret_value = {}
            for k, v in value.items():
                ret_value[k] = self._resolve_variable(key, v, parameters)
            return ret_value
        if isinstance(value, list):
            ret_value = []
            for item in value:
                ret_value.append(self._resolve_variable(key, item, parameters))
            return ret_value
        if isinstance(value, (int, float)):
            return value
        # Check if it's a simple substitution
        match = re.match("^\$\{parameters\.([A-Za-z0-9]+)\}$", value)
        if match:
            variable = match.group(1)
            if variable in parameters:
                return parameters[variable]
            else:
                raise ConfigurationException(
                    f"Failed to parse {key}. Parameters doesn't have {variable}"
                )
        return render(value, parameters)

    @classmethod
    def get_template(cls, template_name):
        split = template_name.split("/")
        if len(split) != 3:
            raise ConfigurationException(f"Incorrect template {template_name}")
        template_id = split[2]
        template_folder = get_or_create_template_folder(template_id)
        template_yaml = load_yaml_from_file(f"{template_folder}/template.yaml")
        return cls(template_id, template_folder, template_yaml)
