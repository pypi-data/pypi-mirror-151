from dataclasses import dataclass
from typing import List, Union, Optional, Iterable

from vtb_authorizer_utils.data_objects import Organization, Project, Folder
from vtb_authorizer_utils.decorators import authorizer_resource_rule
from vtb_authorizer_utils.gateway import AuthorizerGateway


async def get_path(gateway: AuthorizerGateway,
                   context_object: Union[Organization, Project, Folder]) -> Optional[str]:
    """
    Получение полного пути объекта контекста в иерархии
    :param gateway: AuthorizerGateway
    :param context_object: объект контекста
    :return: полный путь объекта контекста в иерархии
    """
    name = context_object.name
    if not name:
        raise ValueError('context_object.name is null or empty.')

    if isinstance(context_object, Organization):
        return f"/organization/{name}/"

    if isinstance(context_object, Project):
        return await gateway.get_project_path(name)

    return await gateway.get_folder_path(name)


@dataclass
class Operation:
    """
    Operation
    """
    view_method: str
    operation_name: str
    url_pattern: Union[str, List[str]]
    access_type: str = "public"
    http_method: str = "get"


def operations_public(operations: Iterable[Operation]):
    """ Operation decorator. """

    def decorator(cls):
        for operation in operations:
            method = getattr(cls, operation.view_method)
            method = authorizer_resource_rule(
                http_method=operation.http_method,
                url_pattern=operation.url_pattern,
                access_type=operation.access_type,
                operation_name=f'{operation.operation_name}')(method)
            setattr(cls, operation.view_method, method)
        return cls

    return decorator
