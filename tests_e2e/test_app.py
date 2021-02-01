import pytest
import os
from threading import Thread
from selenium import webdriver
from dotenv import load_dotenv

from trello import Trello
import app

@pytest.fixture(scope='module')
def test_app():
    load_dotenv(override=True)

    # Create the new board & update the board id environment variable
    trello = Trello()
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
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://127.0.0.1:5000')

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