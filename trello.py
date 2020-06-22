from item import Item
from flask_config import Config
import requests

trello_board_url = 'https://api.trello.com/1/boards/5ef0aa880a06bf1a91b44992/cards'
trello_cards_url = 'https://api.trello.com/1/cards'
todo_list_id = '5ef0aa880a06bf1a91b44993'
done_list_id = '5ef0aa880a06bf1a91b44995'

auth_params = { 'key': Config.TRELLO_API_KEY,'token': Config.TRELLO_API_TOKEN }

def get_trello_card_url(id):
    return f'{trello_cards_url}/{id}'

def map_card_to_item(card):
    status = 'Not Started' if card['idList'] == todo_list_id else 'Completed'
    return Item(card['id'], card['name'], status)


def get_items():
    """
    Fetches all todo list items from Trello.

    Returns:
        list: The list of items.
    """
    
    response = requests.request('GET', trello_board_url, params=auth_params).json()

    return [map_card_to_item(card) for card in response]


def add_item(title):
    """
    Adds a new item with the specified title to Trello.

    Args:
        title: The title of the item.
    """

    requests.request('POST', trello_cards_url, params={**auth_params, 'idList': todo_list_id, 'name': title })


def mark_as_complete(id):
    """
    Moves an item from the To Do list to Done.

    Args:
        item: The item to mark as complete.
    """

    requests.request('PUT', get_trello_card_url(id), params={**auth_params, 'idList': done_list_id })


def remove_item(id):
    """
    Removes an existing item from Trello. 

    Args:
        item: The item to remove.
    """

    requests.request('DELETE', get_trello_card_url(id), params=auth_params)
