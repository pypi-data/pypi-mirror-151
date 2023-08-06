from testlodge.client.base import BaseClient
from testlodge.client.user import UserClient


class Client(UserClient, BaseClient):
    ...
