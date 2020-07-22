import pytest
from dotenv import find_dotenv, load_dotenv
import requests

import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class MockCardsResponse:
    def json():
        return [
            {
                "id": "5f172806e7760645c70be232",
                "idList": "todo-list-id",
                "name": "A name for an item",
                "desc": "Descriptive",
                "dateLastActivity": "2020-07-21T17:38:14.388Z"
            },
            {
                "id": "5f172806e7760645c70be233",
                "idList": "done-list-id",
                "name": "Eat lunch",
                "desc": "Sandwich",
                "dateLastActivity": "2020-07-20T17:38:14.388Z"
            },
            {
                "id": "5f172806e7760645c70be234",
                "idList": "done-list-id",
                "name": "Finish exercise",
                "desc": "1 hour",
                "dateLastActivity": "2020-07-21T12:38:14.388Z"
            },
        ]

@pytest.fixture()
def mock_get_requests(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockCardsResponse

    monkeypatch.setattr(requests, "request", mock_get)


def test_app(mock_get_requests, client):
    response = client.get('/')
    assert response.status_code == 200 

    html_string = str(response.data)
    assert 'A name for an item' in html_string
    assert 'Eat lunch' in html_string
    assert 'Finish exercise' in html_string
