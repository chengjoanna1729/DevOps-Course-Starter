import pytest
import os
from threading import Thread
from selenium import webdriver

from trello import Trello
import app

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    trello = Trello('.env')
    board_id = trello.create_trello_board("Test board")
    os.environ['TRELLO_BOARD_ID'] = board_id

    # construct the new application
    application = app.create_app('.env')

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

    # Create a new item
    add_item_input = driver.find_element_by_name("item_title")
    add_item_input.send_keys("New thing to do")

    add_item_button = driver.find_element_by_xpath('//button[text()="Add item"]')
    add_item_button.click()

    # Complete item
    complete_item_button = driver.find_element_by_xpath('//button[text()="Mark as complete"]')
    complete_item_button.click()

    # Delete item
    delete_item_button = driver.find_element_by_xpath('//button[text()="Delete"]')
    delete_item_button.click()