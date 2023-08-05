import logging

import rich_click as click

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.lib import deployment as deployment_lib
from servicefoundry.build.lib import service as service_lib
from servicefoundry.build.lib import workspace as workspace_lib
from servicefoundry.build.lib.messages import (
    PROMPT_NO_DEPLOYMENTS,
    PROMPT_NO_SERVICES,
    PROMPT_NO_WORKSPACES,
)
from servicefoundry.build.model.entity import (
    Cluster,
    Deployment,
    Secret,
    SecretGroup,
    Service,
    Workspace,
)
from servicefoundry.cli.const import (
    ENABLE_AUTHORIZE_COMMANDS,
    ENABLE_CLUSTER_COMMANDS,
    ENABLE_SECRETS_COMMANDS,
)
from servicefoundry.cli.display_util import print_list
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.group(name="list")
def list_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry list resources

    \b
    Supported resources:
    - workspace
    - service
    - deployment
    """
    pass


@click.command(name="cluster", help="list cluster")
@handle_exception_wrapper
def list_cluster():
    tfs_client = ServiceFoundryServiceClient.get_client()
    clusters = tfs_client.list_cluster()
    print_list("Clusters", clusters, Cluster.display_columns)


@click.command(name="workspace", help="list workspaces")
@click.option("-A", "--all", is_flag=True, default=False)
@click.option("-c", "--cluster", type=click.STRING, default=None, help="cluster name")
@click.option("--non-interactive", is_flag=True, default=False)
@handle_exception_wrapper
def list_workspace(all, cluster, non_interactive):
    # Tests:
    # - Set Context -> list workspace -> Should get workspaces in set cluster
    # - Set Context -> list workspace -c 'cluster_name' -> Should get workspaces in given cluster
    # - Set Context -> list workspace -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - Set Context -> list workspace -A -> Should give all workspaces across all clusters
    # - No Context -> list workspace -c 'cluster_name' -> Should get workspaces in given cluster
    # - No Context -> list workspace -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - No Context -> list workspace -A -> Should give all workspaces across all clusters
    # ? No Context -> list workspace -> Should list workspaces if there is only cluster or ask for cluster name
    workspaces = workspace_lib.list_workspaces(
        cluster_name_or_id=cluster,
        all_=all,
        non_interactive=non_interactive,
    )
    if not workspaces:
        console.print(PROMPT_NO_WORKSPACES)
    else:
        workspaces.sort(key=lambda w: (w.fqn, w.createdAt))
    # TODO (chiragjn): Display columns here need to show cluster name!
    print_list(
        "Workspaces",
        [w.to_dict() for w in workspaces],
        columns=Workspace.display_columns,
    )


@click.command(name="service", help="list service in a workspace")
@click.option("-A", "--all", is_flag=True, default=False)
@click.option(
    "-w", "--workspace", type=click.STRING, default=None, help="workspace name"
)
@click.option("-c", "--cluster", type=click.STRING, default=None, help="cluster name")
@click.option("--non-interactive", is_flag=True, default=False)
@handle_exception_wrapper
def list_service(all, workspace, cluster, non_interactive):
    services = service_lib.list_services(
        workspace_name_or_id=workspace,
        cluster_name_or_id=cluster,
        all_=all,
        non_interactive=non_interactive,
    )
    if not services:
        console.print(PROMPT_NO_SERVICES)
    else:
        services.sort(key=lambda s: (s.fqn, s.name))
    # TODO (chiragjn): Display columns here need to show workspace and cluster name!
    print_list(
        f"Services",
        [s.to_dict() for s in services],
        columns=Service.display_columns,
    )


@click.command(name="deployment", help="list deployment")
@click.argument("service")
@click.option(
    "-w", "--workspace", type=click.STRING, default=None, help="workspace name"
)
@click.option("-c", "--cluster", type=click.STRING, default=None, help="cluster name")
@click.option("--non-interactive", is_flag=True, default=False)
@handle_exception_wrapper
def list_deployment(service, workspace, cluster, non_interactive):
    deployments = deployment_lib.list_deployments(
        service_name_or_id=service,
        workspace_name_or_id=workspace,
        cluster_name_or_id=cluster,
        all_=False,  # TODO (chirajn): Add support for all flag
        non_interactive=non_interactive,
    )
    if not deployments:
        console.print(PROMPT_NO_DEPLOYMENTS)
    else:
        deployments.sort(key=lambda d: (d.fqn, d.name))
    print_list(
        f"Deployments",
        [d.to_dict() for d in deployments],
        columns=Deployment.display_columns,
    )


@click.command(name="secret-group", help="list secret groups")
@handle_exception_wrapper
def list_secret_group():
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_secret_groups()
    print_list("Secret Groups", response, columns=SecretGroup.display_columns)


@click.command(name="secret", help="list secrets in a group")
@click.argument("secret_group_id")
@handle_exception_wrapper
def list_secret(secret_group_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_secrets_in_group(secret_group_id)
    print_list("Secrets", response, columns=Secret.display_columns)


@click.command(name="authorize", help="list authorization for a resource id.")
@click.argument("resource_type", type=click.Choice(["workspace"], case_sensitive=False))
@click.argument("resource_id")
@handle_exception_wrapper
def list_authorize(resource_type, resource_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_authorization_for_resource(resource_type, resource_id)
    print_list(f"Auth for {resource_type}: {resource_id}", response)


def get_list_command():
    list_command.add_command(list_workspace)
    list_command.add_command(list_service)
    list_command.add_command(list_deployment)

    if ENABLE_AUTHORIZE_COMMANDS:
        list_command.add_command(list_authorize)
    if ENABLE_CLUSTER_COMMANDS:
        list_command.add_command(list_cluster)
    if ENABLE_SECRETS_COMMANDS:
        list_command.add_command(list_secret)
        list_command.add_command(list_secret_group)

    return list_command
