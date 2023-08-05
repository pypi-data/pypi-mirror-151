from furl import Path as UrlPath
from furl.furl import furl as Url
from requests.models import Response
from testlodge._types import Identifier
from testlodge.api.base import BaseAPI
from testlodge.models.custom_field import CustomFieldListJSON


class CustomFieldAPI(BaseAPI):
    """API for custom fields.

    Endpoints
    ---------
    * List
    """

    name: str = 'custom_field'

    def _list(
        self,
        project_id: Identifier,
    ) -> CustomFieldListJSON:
        """List all custom fields in a project.

        Parameters
        ----------
        project_id: Identifier
            The ID of the project.
        """

        method = 'GET'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}' '/custom_fields.json'
        )

        response: Response = self.client._request(
            method=method,
            url=url,
        )
        custom_field_list: CustomFieldListJSON = response.json()

        return custom_field_list

    def _create(self):
        """Create custom fields."""
        raise NotImplementedError("This action is not supported.")
