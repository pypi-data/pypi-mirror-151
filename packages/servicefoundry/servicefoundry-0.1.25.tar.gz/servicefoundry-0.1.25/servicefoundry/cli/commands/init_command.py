import logging
from types import SimpleNamespace

import questionary
import rich_click as click
from questionary import Choice

from servicefoundry.build import lib
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.session_factory import get_session
from servicefoundry.build.template.sf_template import SfTemplate
from servicefoundry.build.template.template_workflow import TemplateWorkflow
from servicefoundry.build.util import BadRequestException
from servicefoundry.cli.commands.cli_input_hook import CliInputHook
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.command(help="Initialize new service for servicefoundry")
@handle_exception_wrapper
def init():
    # Get SFSClient
    tfs_client = ServiceFoundryServiceClient.get_client()

    # Get Session else do login
    try:
        get_session()
    except BadRequestException:
        do_login = questionary.select(
            "You need to login to create a service", ["Login", "Exit"]
        ).ask()
        if do_login == "Login":
            lib.login(non_interactive=False)
        else:
            return

    # Static call to get list of templates
    templates = tfs_client.get_templates_list()

    # Choose a template of service to be created.
    template_choices = [
        Choice(f'{t["id"]} - {t["description"]}', value=t["id"]) for t in templates
    ]
    template_id = questionary.select("Choose a template", template_choices).ask()
    sf_template = SfTemplate.get_template(f"truefoundry.com/v1/{template_id}")
    template_workflow = TemplateWorkflow(sf_template, CliInputHook(tfs_client))
    template_workflow.process_parameter()
    template_workflow.write()

    if sf_template.post_init_instruction:
        console.print(
            sf_template.post_init_instruction.format(
                parameters=SimpleNamespace(**template_workflow.parameters)
            )
        )


def get_init_command():
    return init
