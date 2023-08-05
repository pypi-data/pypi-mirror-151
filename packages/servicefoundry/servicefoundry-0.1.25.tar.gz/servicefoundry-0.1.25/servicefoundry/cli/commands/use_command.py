import logging

import rich_click as click

from servicefoundry.build.lib import context as context_lib
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.group(name="use")
def use_command():
    """
    Set default workspace

    \b
    Supported resources:
    - workspace
    - cluster
    """
    pass


@click.command(name="cluster", help="Set default cluster")
@click.argument("cluster", type=click.STRING, required=False, default=None)
@click.option("--non-interactive", is_flag=True, default=False)
@handle_exception_wrapper
def use_cluster(cluster, non_interactive):
    context_lib.use_cluster(name_or_id=cluster, non_interactive=non_interactive)


@click.command(name="workspace", help="Set default workspace")
@click.argument("workspace", type=click.STRING, required=False, default=None)
@click.option("--non-interactive", is_flag=True, default=False)
@handle_exception_wrapper
def use_workspace(workspace, non_interactive):
    context_lib.use_workspace(
        name_or_id=workspace,
        cluster_name_or_id=None,  # pick from context if available
        non_interactive=non_interactive,
    )


def get_set_command():
    use_command.add_command(use_cluster)
    use_command.add_command(use_workspace)
    return use_command
