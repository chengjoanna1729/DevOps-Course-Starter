from to_do_item import ToDoItem, Status
from trello_config import Config
import requests

config = Config('.env')

trello_board_url = f'https://api.trello.com/1/boards/{config.board_id}/cards'
trello_cards_url = 'https://api.trello.com/1/cards'
auth_params = { 'key': config.api_key, 'token': config.api_token }

def get_status(list_id):
    if list_id == config.todo_list_id:
        return Status.TO_DO
    elif list_id == config.doing_list_id:
        return Status.DOING
    else:
        return Status.DONE

def get_trello_card_url(id):
    return f'{trello_cards_url}/{id}'

def get_items():
    """
    Fetches all todo list items from Trello.

    Returns:
        list: The list of items.
    """
    
    response = requests.request('GET', trello_board_url, params=auth_params).json()
    
    return [ToDoItem.fromTrelloCard(card, get_status(card['idList'])) for card in response]


def add_item(title, description = ''):
    """
    Adds a new item with the specified title and optional description to Trello.

    Args:
        title: The title of the item.
        description: The description of the item
    """

    requests.request('POST', trello_cards_url, params={**auth_params, 'idList': config.todo_list_id, 'name': title, 'desc': description })


def mark_as_complete(id):
    """
    Moves an item from the To Do list to Done.

    Args:
        id: The id of the item to mark as complete.
    """

    requests.request('PUT', get_trello_card_url(id), params={**auth_params, 'idList': config.done_list_id })


def remove_item(id):
    """
    Removes an existing item from Trello. 

    Args:
        id: The id of the item to remove.
    """

    requests.request('DELETE', get_trello_card_url(id), params=auth_params)
