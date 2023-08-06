from testlodge.api.user import UserAPI
from testlodge.client.base import BaseClient
from testlodge.typing.user import UserListJSON


class UserClient(BaseClient):
    def get_user_list_json(self, page: int = 1) -> UserListJSON:
        return getattr(self.api, UserAPI.name)._list(page)
