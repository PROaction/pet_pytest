import allure
import pytest
import requests
from typing_extensions import Any, Optional

BASE_ADDRESS = 'http://users.bugred.ru/tasks/rest'


class ApiServer:
    """Base class."""

    def __init__(self, base_address):
        self._base_address = base_address
        self._headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }

        # common fields
        self.count_body_fields = None
        self.http_status = None
        self.type = None
        self.message = None

    def _definition_fields(self, response: Optional[Any]) -> None:
        """Get fields from response."""
        response_body = response.json()

        self.type = response_body.get('type')
        self.message = response_body.get('message')

        self.http_status = response.status_code
        self.count_body_fields = len(response_body)


class Users(ApiServer):
    """Class for implementing user methods."""

    def __init__(self, base_address):
        super().__init__(base_address)

        # common doregister\getuser\getuserfull
        self.date_start = None
        self.hobby = None
        self.gender = None
        self.birthday = None
        self.email = None
        self.password = None
        self.avatar = None
        self.name = None

        # getuserfull
        self.tasks = None
        self.companys = None

    def _definition_fields(self, response: Optional[Any]) -> None:
        """Get fields from response."""
        super()._definition_fields(response)
        response_body = response.json()

        self.name = response_body.get('name')
        self.avatar = response_body.get('avatar')
        self.password = response_body.get('password')
        self.birthday = response_body.get('birthday')
        self.email = response_body.get('email')
        self.gender = response_body.get('gender')
        self.date_start = response_body.get('date_start')
        self.hobby = response_body.get('hobby')
        self.tasks = response_body.get('tasks')
        self.companys = response_body.get('companys')

    def doregister(self, path='/doregister', json=None):
        """Implementing REST-API method POST /doregister."""
        url = f'{self._base_address}{path}'

        with allure.step(f'Send request POST {url}'):
            response = requests.post(
                url=url,
                json=json,
                headers=self._headers
            )
        self._definition_fields(response)

    def getuser(self, path='/getuser', json=None):
        """Implementing REST-API method POST /getuser."""
        url = f'{self._base_address}{path}'

        with allure.step(f'Send request POST {url}'):
            response = requests.post(
                url=url,
                json=json,
                headers=self._headers
            )

        self._definition_fields(response)

    def useronefield(self, path='/useronefield', json=None):
        """Implementing REST-API method POST /useronefield."""
        url = f'{self._base_address}{path}'

        with allure.step(f'Send request POST {url}'):
            response = requests.post(
                url=url,
                json=json,
                headers=self._headers
            )

        self._definition_fields(response)

    def getuserfull(self, path='/getuserfull', json=None):
        """Implementing REST-API method POST /getuserfull."""
        url = f'{self._base_address}{path}'

        with allure.step(f'Send request POST {url}'):
            response = requests.post(
                url=url,
                json=json,
                headers=self._headers
            )

        self._definition_fields(response)


class Tasks(ApiServer):
    """Class for implementing Tasks methods."""

    def __init__(self, base_address):
        super().__init__(base_address)

    def _definition_fields(self, response):
        """Get fields from response."""
        super()._definition_fields(response)
        response_body = response.json()

        # createtask field
        self.id_task = response_body.get('id_task')

    def createtask(self, path='/createtask', json=None):
        """Implementing REST-API method POST /createtask."""
        url = f'{self._base_address}{path}'

        with allure.step(f'Send request POST {url}'):
            response = requests.post(
                url=url,
                json=json,
                headers=self._headers
            )

        self._definition_fields(response)


def deleteuser(path='/deleteuser', json=None) -> None:
    """Method for removing the user after passing the test."""
    url = f'{BASE_ADDRESS}{path}'

    requests.post(
        url=url,
        json=json,
    )


def deletetask(path='/deletetask', json=None) -> None:
    """Method for deleting a task after passing a test."""
    url = f'{BASE_ADDRESS}{path}'

    requests.post(
        url=url,
        json=json,
    )


@pytest.fixture()
def users_api(request):
    """Users interface."""
    return Users(base_address=BASE_ADDRESS)


@pytest.fixture()
def tasks_api(request):
    """Tasks interface."""
    return Tasks(base_address=BASE_ADDRESS)


@pytest.fixture()
def delete_user_after_test(request):
    """User removal feature after passing the test."""
    yield

    email = request.node.email
    print(f'User with email - \'{email}\' deleted.')
    json = {
        'email': email
    }
    deleteuser(json=json)


@pytest.fixture()
def delete_task_after_test(request):
    """Task removal feature after passing the test."""
    yield

    email_owner = request.node.email_owner
    id_task = request.node.id_task
    print(f'Task with owner - \'{email_owner}\' '
          f'and task_id - {id_task} deleted.')
    json = {
        "email_owner": email_owner,
        "task_id": id_task
    }
    deleteuser(json=json)
