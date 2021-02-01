import pytest
import requests
import lxml.html
from dotenv import load_dotenv
from trello import Trello

import app

@pytest.fixture
def client():
    # Use test env variables
    load_dotenv('.env.test')

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

MockListsResponse = [
    {
        "id": "todo-list-id",
        "name": "To Do"
    },
    {
        "id": "doing-list-id",
        "name": "Doing"
    },
    {
        "id": "done-list-id",
        "name": "Done"
    },
]
            

@pytest.fixture()
def mock_requests(monkeypatch):
    def mock_get_cards(*args, **kwargs):
        return MockCardsResponse
        
    def mock_get_lists(*args, **kwargs):
        return MockListsResponse

    monkeypatch.setattr(requests, "request", mock_get_cards)
    monkeypatch.setattr(Trello, "get_lists", mock_get_lists)


def test_app(mock_requests, client):
    response = client.get('/')
    assert response.status_code == 200 

    tree = lxml.html.fromstring(response.data)
    assert ['A name for an item', 'Eat lunch', 'Finish exercise'] == tree.xpath("//li[@class='list-group-item']/div/span/text()")
