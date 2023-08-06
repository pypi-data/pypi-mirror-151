from testlodge.client.base import BaseClient
from testlodge.client.project import ProjectClient
from testlodge.client.user import UserClient


class Client(UserClient, ProjectClient, BaseClient):
    ...


__all__ = ['Client']
