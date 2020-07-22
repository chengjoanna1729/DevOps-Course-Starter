import pytest
import os
from threading import Thread
from selenium import webdriver

import trello
import app

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    board_id = trello.create_trello_board("Test board")
    os.environ['TRELLO_BOARD_ID'] = board_id

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    trello.delete_trello_board(board_id)

@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000')

    assert driver.title == 'To-Do App'

    # TODO: assert more things
    