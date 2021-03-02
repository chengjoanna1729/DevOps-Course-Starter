import pytest
import requests
import lxml.html
from dotenv import find_dotenv, load_dotenv
from mongodb import MongoDB
import pymongo

import app

@pytest.fixture
def client():
    # Use test env variables
    load_dotenv(find_dotenv('.env.test'), override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

mock_collection_items = [
    {
        "_id": "5f172806e7760645c70be232",
        "name": "A name for an item",
        "status": "To Do",
        "dateLastActivity": "2020-07-21T17:38:14.388Z"
    },
    {
        "_id": "5f172806e7760645c70be233",
        "name": "Eat lunch",
        "status": "Done",
        "dateLastActivity": "2020-07-20T17:38:14.388Z"
    },
    {
        "_id": "5f172806e7760645c70be234",
        "name": "Finish exercise",
        "status": "Done",
        "dateLastActivity": "2020-07-21T12:38:14.388Z"
    },
]

@pytest.fixture()
def mock_requests(monkeypatch):
    def mock_get_collection_items(*args, **kwargs):
        return mock_collection_items
    
    def mock_get_client(*args, **kwargs):
        return { "test-db": { "all_todos" : {} } }

    monkeypatch.setattr(MongoDB, "get_collection_items", mock_get_collection_items)
    monkeypatch.setattr(pymongo, "MongoClient", mock_get_client)


def test_app(mock_requests, client):
    response = client.get('/')
    assert response.status_code == 200 

    tree = lxml.html.fromstring(response.data)
    assert ['A name for an item', 'Eat lunch', 'Finish exercise'] == tree.xpath("//li[@class='list-group-item']/div/span/text()")
