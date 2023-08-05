from typing import Optional, List, Union, Tuple, TypeVar

import questionary

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.lib.messages import (
    PROMPT_USING_CLUSTER_CONTEXT,
    PROMPT_USING_WORKSPACE_CONTEXT,
)
from servicefoundry.build.model.entity import Cluster, Workspace, Service, Deployment

# TODO: Move type casting downwards into `ServiceFoundrySession` and `ServiceFoundryServiceClient`
# TODO: Abstract duplicated code across resolving different entities
T = TypeVar("T")


def _filter_by_name_or_id(instances: List[T], name_or_id: Optional[str]) -> List[T]:
    if name_or_id:
        found = [i for i in instances if i.name == name_or_id]
        if not found:
            found = [i for i in instances if i.id == name_or_id]
    else:
        found = instances
    return found


def resolve_clusters(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    ignore_context: bool = False,
) -> List[Cluster]:
    if not ignore_context and not name_or_id:
        cluster = client.session.get_cluster()
        if cluster:
            cluster = Cluster.from_dict(cluster)
            return [cluster]
    clusters = [Cluster.from_dict(c) for c in client.list_cluster()]
    return _filter_by_name_or_id(instances=clusters, name_or_id=name_or_id)


def resolve_workspaces(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
) -> List[Workspace]:
    if not ignore_context and not name_or_id:
        workspace = client.session.get_workspace()
        if workspace:
            workspace = Workspace.from_dict(workspace)
            return [workspace]

    if isinstance(cluster_name_or_id, Cluster):
        clusters = [cluster_name_or_id]
        cluster_name_or_id = clusters[0].id
    else:
        clusters = resolve_clusters(
            client=client, name_or_id=cluster_name_or_id, ignore_context=ignore_context
        )

    if not clusters:
        if cluster_name_or_id:
            raise ValueError(f"No cluster found with name or id {cluster_name_or_id!r}")
        else:
            workspaces = [Workspace.from_dict(w) for w in client.list_workspace()]
    elif len(clusters) > 1:
        raise ValueError(
            f"More than one cluster found with name or id {cluster_name_or_id!r}: {clusters!r}"
        )
    else:
        cluster = clusters[0]
        _workspaces = client.get_workspace_by_name(
            workspace_name="", cluster_id=cluster.id
        )
        workspaces = [Workspace.from_dict(w) for w in _workspaces]
    return _filter_by_name_or_id(instances=workspaces, name_or_id=name_or_id)


def resolve_services(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    workspace_name_or_id: Optional[Union[Workspace, str]] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
) -> List[Service]:
    if isinstance(workspace_name_or_id, Workspace):
        workspaces = [workspace_name_or_id]
        workspace_name_or_id = workspaces[0].id
    else:
        workspaces = resolve_workspaces(
            client=client,
            name_or_id=workspace_name_or_id,
            cluster_name_or_id=cluster_name_or_id,
            ignore_context=ignore_context,
        )
    if not workspaces:
        if workspace_name_or_id:
            raise ValueError(
                f"No workspaces found with name or id {workspace_name_or_id!r}"
            )
        else:
            services = [Service.from_dict(s) for s in client.list_service()]
    elif len(workspaces) > 1:
        raise ValueError(
            f"More than one workspace found with name or id {workspace_name_or_id!r}: {workspaces!r}"
        )
    else:
        workspace = workspaces[0]
        _services = client.list_service_by_workspace(workspace_id=workspace.id)
        services = [Service.from_dict(s) for s in _services]
    return _filter_by_name_or_id(instances=services, name_or_id=name_or_id)


def resolve_deployments(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    service_name_or_id: Optional[Union[Service, str]] = None,
    workspace_name_or_id: Optional[Union[Workspace, str]] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
) -> List[Deployment]:
    if isinstance(service_name_or_id, Service):
        services = [service_name_or_id]
        service_name_or_id = services[0].id
    else:
        services = resolve_services(
            client=client,
            name_or_id=service_name_or_id,
            workspace_name_or_id=workspace_name_or_id,
            cluster_name_or_id=cluster_name_or_id,
            ignore_context=ignore_context,
        )
    if not services:
        if service_name_or_id:
            raise ValueError(
                f"No services found with name or id {service_name_or_id!r}"
            )
        else:
            # TODO (chiragjn): Needs an API from server side to fetch all deployments.
            #                  Otherwise we can do it slowly by doing
            #                  flatten([c.list_deployment(service_id=s.id) for s in all_services])
            raise NotImplementedError(
                "Cannot fetch deployments without a service name or id"
            )
    elif len(services) > 1:
        raise ValueError(
            f"More than one service found with name or id {service_name_or_id!r}: {services!r}"
        )
    else:
        service = services[0]
        _deployments = client.list_deployment(service_id=service.id)
        deployments = [Deployment.from_dict(d) for d in _deployments]
    return _filter_by_name_or_id(instances=deployments, name_or_id=name_or_id)


def ask_pick_cluster(clusters: List[Cluster]) -> Cluster:
    choices = [
        questionary.Choice(title=f"{c.name} ({c.fqn})", value=c) for c in clusters
    ]
    return questionary.select("Pick a cluster", choices=choices).ask()


def maybe_ask_pick_cluster(clusters: List[Cluster]) -> Cluster:
    if len(clusters) == 1:
        return clusters[0]
    return ask_pick_cluster(clusters=clusters)


def ask_pick_workspace(workspaces: List[Workspace]) -> Workspace:
    choices = [
        questionary.Choice(title=f"{w.name} ({w.fqn})", value=w) for w in workspaces
    ]
    return questionary.select("Pick a workspace", choices=choices).ask()


def maybe_ask_pick_workspace(workspaces: List[Workspace]) -> Workspace:
    if len(workspaces) == 1:
        return workspaces[0]
    return ask_pick_workspace(workspaces=workspaces)


def ask_pick_service(services: List[Service]) -> Service:
    choices = [
        questionary.Choice(title=f"{s.name} ({s.fqn})", value=s) for s in services
    ]
    return questionary.select("Pick a service", choices=choices).ask()


def maybe_ask_pick_service(services: List[Service]) -> Service:
    if len(services) == 1:
        return services[0]
    return ask_pick_service(services=services)


def ask_pick_deployment(deployments: List[Deployment]) -> Deployment:
    choices = [
        questionary.Choice(title=f"{d.name} ({d.fqn})", value=d) for d in deployments
    ]
    return questionary.select("Pick a deployment", choices=choices).ask()


def maybe_ask_pick_deployment(deployments: List[Deployment]) -> Deployment:
    if len(deployments) == 1:
        return deployments[0]
    return ask_pick_deployment(deployments=deployments)


def resolve_cluster_or_error(
    name_or_id: Optional[str] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Cluster:
    if non_interactive:
        if ignore_context and not name_or_id:
            raise ValueError(
                "cluster name or id cannot be null. Pass it using `--cluster` or `-c`"
            )

    clusters = resolve_clusters(
        client=client, name_or_id=name_or_id, ignore_context=ignore_context
    )

    if not clusters:
        if name_or_id:
            raise ValueError(f"No cluster found with name or id {name_or_id!r}")
        else:
            raise ValueError(f"No clusters found!")
    else:
        if non_interactive:
            if len(clusters) > 1:
                raise ValueError(
                    f"More than one cluster found with name or id {name_or_id!r}: {clusters!r}"
                )
            else:
                cluster = clusters[0]
        else:
            cluster = maybe_ask_pick_cluster(clusters=clusters)
    return cluster


def resolve_workspace_or_error(
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Tuple[Workspace, Cluster]:
    if non_interactive:
        if ignore_context and not name_or_id:
            raise ValueError(
                "workspace name or id cannot be null. Pass it using `--workspace` or `-w`"
            )

    if isinstance(cluster_name_or_id, Cluster):
        cluster = cluster_name_or_id
    else:
        cluster = resolve_cluster_or_error(
            name_or_id=cluster_name_or_id,
            non_interactive=non_interactive,
            ignore_context=ignore_context,
            client=client,
        )

    console.print(PROMPT_USING_CLUSTER_CONTEXT.format(cluster.name))

    workspaces = resolve_workspaces(
        client=client,
        name_or_id=name_or_id,
        cluster_name_or_id=cluster,
        ignore_context=ignore_context,
    )
    if not workspaces:
        if name_or_id:
            raise ValueError(
                f"No workspace found with name or id {name_or_id!r} in cluster {cluster.name!r}"
            )
        else:
            raise ValueError(f"No workspaces found!")
    else:
        if non_interactive:
            if len(workspaces) > 1:
                raise ValueError(
                    f"More than one workspace found with name or id {name_or_id!r}: {workspaces!r}"
                )
            else:
                workspace = workspaces[0]
        else:
            workspace = maybe_ask_pick_workspace(workspaces=workspaces)
    return workspace, cluster


def resolve_service_or_error(
    name_or_id: str,
    workspace_name_or_id: Optional[Union[Workspace, str]] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Tuple[Service, Workspace, Cluster]:
    if non_interactive:
        if ignore_context and not name_or_id:
            raise ValueError("service name or id cannot be null")

    if isinstance(cluster_name_or_id, Cluster):
        cluster = cluster_name_or_id
    else:
        cluster = resolve_cluster_or_error(
            name_or_id=cluster_name_or_id,
            non_interactive=non_interactive,
            ignore_context=ignore_context,
            client=client,
        )

    if isinstance(workspace_name_or_id, Workspace):
        workspace = workspace_name_or_id
    else:
        workspace, cluster = resolve_workspace_or_error(
            name_or_id=workspace_name_or_id,
            cluster_name_or_id=cluster,
            non_interactive=non_interactive,
            ignore_context=ignore_context,
            client=client,
        )

    console.print(PROMPT_USING_WORKSPACE_CONTEXT.format(workspace.name))

    services = resolve_services(
        client=client,
        name_or_id=name_or_id,
        workspace_name_or_id=workspace,
        cluster_name_or_id=cluster,
        ignore_context=ignore_context,
    )

    if not services:
        if name_or_id:
            raise ValueError(
                f"No service found with name or id {name_or_id!r} in workspace {workspace.name!r}"
            )
        else:
            raise ValueError(f"No services found!")
    else:
        if non_interactive:
            if len(services) > 1:
                raise ValueError(
                    f"More than one service found with name or id {name_or_id!r}: {services!r}"
                )
            else:
                service = services[0]
        else:
            service = maybe_ask_pick_service(services=services)

    return service, workspace, cluster


def resolve_deployment_or_error(
    name_or_id: str,
    service_name_or_id: Optional[Union[Service, str]] = None,
    workspace_name_or_id: Optional[Union[Workspace, str]] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Tuple[Deployment, Service, Workspace, Cluster]:
    if non_interactive:
        if ignore_context and not name_or_id:
            raise ValueError("deployment name or id cannot be null")

    # TODO: resolve separately if we start to have a get all deployments API that can give deployments across services
    service, workspace, cluster = resolve_service_or_error(
        name_or_id=service_name_or_id,
        workspace_name_or_id=workspace_name_or_id,
        cluster_name_or_id=cluster_name_or_id,
        ignore_context=ignore_context,
        non_interactive=non_interactive,
        client=client,
    )

    deployments = resolve_deployments(
        client=client,
        service_name_or_id=service,
        name_or_id=name_or_id,
        workspace_name_or_id=workspace,
        cluster_name_or_id=cluster,
        ignore_context=ignore_context,
    )

    if not deployments:
        if name_or_id:
            raise ValueError(
                f"No deployment found with name or id {name_or_id!r} for service {service.name!r}"
            )
        else:
            raise ValueError(f"No deployments found!")
    else:
        if non_interactive:
            if len(deployments) > 1:
                raise ValueError(
                    f"More than one deployment found with name or id {name_or_id!r}: {deployments!r}"
                )
            else:
                deployment = deployments[0]
        else:
            deployment = maybe_ask_pick_deployment(deployments=deployments)

    return deployment, service, workspace, cluster
