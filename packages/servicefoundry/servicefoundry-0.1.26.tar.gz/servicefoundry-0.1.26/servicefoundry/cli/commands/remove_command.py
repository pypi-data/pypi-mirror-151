import logging

import questionary
import rich_click as click
from rich import print_json

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.lib import service as service_lib
from servicefoundry.build.lib import workspace as workspace_lib
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import (
    ENABLE_AUTHORIZE_COMMANDS,
    ENABLE_CLUSTER_COMMANDS,
    ENABLE_SECRETS_COMMANDS,
)
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.group(name="remove")
def remove_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry remove entity by id

    \b
    Supported resources:
    - workspace
    - service
    """
    pass


@click.command(name="cluster", help="remove cluster")
@click.argument("cluster_id")
@handle_exception_wrapper
def remove_cluster(cluster_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove cluster {cluster_id!r}?",
    ).ask()
    if confirm:
        tfs_client.remove_cluster(cluster_id)
        # Remove workspace and cluster from context
        ctx_cluster = tfs_client.session.get_cluster()
        if ctx_cluster and ctx_cluster["id"] == cluster_id:
            tfs_client.session.set_workspace(None)
            tfs_client.session.set_cluster(None)
            tfs_client.session.save_session()
    else:
        raise Exception("Aborted!")


@click.command(name="workspace", help="remove workspace")
@click.argument("name", type=click.STRING)
@click.option(
    "-c",
    "--cluster",
    type=click.STRING,
    default=None,
    help="cluster to remove the workspace from",
)
@click.confirmation_option(prompt="Are you sure you want to remove this workspace?")
@handle_exception_wrapper
def remove_workspace(name, cluster):
    # Tests:
    # - Set Context -> remove workspace -> Should give error to give workspace name
    # - Set Context -> remove workspace valid_name -> Should delete
    # - Set Context -> remove workspace invalid_name -> Should give error no such workspace in set cluster
    # - Set Context -> remove workspace name -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - Set Context -> remove workspace invalid_name -c 'cluster_name' -> Should give error invalid workspace
    # - Set Context -> remove workspace valid_name -c 'cluster_name' -> Should delete
    # - No Context -> remove workspace -> Should give error to give workspace name
    # - No Context -> remove workspace valid_name -> Try to resolve, if only one exists then delete
    #                 otherwise error to give cluster
    # - No Context -> remove workspace invalid_name -> Tries to resolve, if only one exists then delete
    #                 otherwise error to give cluster
    # - No Context -> remove workspace name -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - No Context -> remove workspace invalid_name -c 'cluster_name' -> Should give error invalid workspace
    # - No Context -> remove workspace valid_name -c 'cluster_name' -> Should delete
    tail_logs = not CliConfig.get("json")
    response = workspace_lib.remove_workspace(
        name_or_id=name,
        cluster_name_or_id=cluster,
        tail_logs=tail_logs,
        non_interactive=True,
    )
    if not tail_logs:
        print_json(data=response)


@click.command(name="service", help="remove service")
@click.argument("name", type=click.STRING)
@click.option(
    "-w",
    "--workspace",
    type=click.STRING,
    default=None,
    help="workspace to find this service in",
)
@click.option(
    "-c",
    "--cluster",
    type=click.STRING,
    default=None,
    help="cluster to find this cluster in",
)
@click.confirmation_option(prompt="Are you sure you want to remove this service?")
@handle_exception_wrapper
def remove_service(name, workspace, cluster):
    tail_logs = not CliConfig.get("json")
    response = service_lib.remove_service(
        name_or_id=name,
        workspace_name_or_id=workspace,
        cluster_name_or_id=cluster,
        tail_logs=tail_logs,
        non_interactive=True,
    )
    if not tail_logs:
        print_json(data=response)


@click.command(name="secret-group", help="remove secret-group")
@click.argument("secret_group_id")
@handle_exception_wrapper
def remove_secret_group(secret_group_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove secret group {secret_group_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        response = tfs_client.delete_secret_group(secret_group_id)
        print_json(data=response)
    else:
        raise Exception("Aborted!")


@click.command(name="secret", help="remove secret")
@click.argument("secret_id")
@handle_exception_wrapper
def remove_secret(secret_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove secret {secret_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        response = tfs_client.delete_secret(secret_id)
        print_json(data=response)
    else:
        raise Exception("Aborted!")


@click.command(name="auth", help="remove authorization")
@click.argument("authorization_id")
@handle_exception_wrapper
def remove_auth(authorization_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove authorization {authorization_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        response = tfs_client.delete_authorization(authorization_id)
        print_json(data=response)
    else:
        raise Exception("Aborted!")


def get_remove_command():
    remove_command.add_command(remove_workspace)
    remove_command.add_command(remove_service)

    if ENABLE_AUTHORIZE_COMMANDS:
        remove_command.add_command(remove_auth)

    if ENABLE_CLUSTER_COMMANDS:
        remove_command.add_command(remove_cluster)

    if ENABLE_SECRETS_COMMANDS:
        remove_command.add_command(remove_secret)
        remove_command.add_command(remove_secret_group)

    return remove_command
