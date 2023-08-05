from furl import Path as UrlPath
from furl.furl import furl as Url
from requests.models import Response
from testlodge.api.base import BaseAPI
from testlodge.api.common import SortOrder
from testlodge.models.suite import SuiteJSON
from testlodge.models.suite import SuiteListJSON


class SuiteAPI(BaseAPI):
    """API for test suites.

    Endpoints
    ---------
    * List
    * Show
    * Create
    * Update
    * Delete
    """

    name: str = 'suite'

    def _list(
        self,
        project_id: int,
        page: int = 1,
        order: SortOrder = SortOrder.CREATED_AT,
    ) -> SuiteListJSON:
        """Paginated list of all suites in a project.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        page: int, default=1
            Default: 1
            The number of the page to return.
        order: SortOrder, default=SortOrder.CREATED_AT
            Default: SortOrder.CREATED_AT
            Method to sort the list of suites.
        """

        method = 'GET'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}' '/suites.json'
        )
        params: dict = {}
        if page != 1:
            params['page'] = page
        if order != SortOrder.CREATED_AT:
            params['order'] = int(order)

        response: Response = self.client._request(
            method=method, url=url, params=params
        )
        suite_list: SuiteListJSON = response.json()

        return suite_list

    def _show(
        self,
        project_id: int,
        suite_id: int,
    ) -> SuiteJSON:
        """Get the details for a suite.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        suite_id: int
            The ID of the suite.
        """

        method = 'GET'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}' f'/suites/{suite_id}.json'
        )

        response: Response = self.client._request(
            method=method,
            url=url,
        )
        suite_json: SuiteJSON = response.json()

        return suite_json

    def _create(
        self,
        project_id: int,
        suite: SuiteJSON,
    ) -> SuiteJSON:
        """Create a suite.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        suite: SuiteJSON

            name: str
                Name of the suite.
            plan_id: int, optional
                Associated test plan.
        """

        method = 'POST'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}' '/suites.json'
        )

        data = dict(suite=suite)

        response: Response = self.client._request(
            method=method, url=url, json=data
        )
        suite_json: SuiteJSON = response.json()

        return suite_json

    def _update(
        self,
        project_id: int,
        suite_id: int,
        suite: SuiteJSON,
    ) -> SuiteJSON:
        """Update a suite.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        suite_id: int
            The ID of the suite.
        suite: SuiteJSON

            name: str
                Name of the suite.
            plan_id: int
                Associated test plan.
        """

        method = 'PATCH'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}' f'/suites/{suite_id}.json'
        )
        data = dict(suite=suite)

        response: Response = self.client._request(
            method=method,
            url=url,
            json=data,
        )
        suite_json: SuiteJSON = response.json()

        return suite_json

    def _delete(
        self,
        project_id: int,
        suite_id: int,
    ) -> None:
        """Delete a suite.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        suite_id: int
            The ID of the suite.
        """

        method = 'DELETE'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}' f'/suites/{suite_id}.json'
        )

        response: Response = self.client._request(method=method, url=url)

        status_code: int = response.status_code
        if status_code != 204:
            print(f'Unexpected response code: {status_code}')

        return None
