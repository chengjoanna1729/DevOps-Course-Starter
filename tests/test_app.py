import pytest
import requests
import lxml.html

import app

@pytest.fixture
def client():
    # Create the new app.
    test_app = app.create_app('.env.test')

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
def mock_requests(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockCardsResponse

    monkeypatch.setattr(requests, "request", mock_get)


def test_app(mock_requests, client):
    response = client.get('/')
    assert response.status_code == 200 

    tree = lxml.html.fromstring(response.data)
    assert ['A name for an item', 'Eat lunch', 'Finish exercise'] == tree.xpath("//li[@class='list-group-item']/div/span/text()")
