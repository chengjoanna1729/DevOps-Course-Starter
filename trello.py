from to_do_item import ToDoItem, Status
from trello_config import Config
import requests

class Trello:
    def __init__(self, dotenv):
        self.config = Config(dotenv)
        self.trello_base_url = 'https://api.trello.com/1'
        self.trello_board_url = f'{self.trello_base_url}/boards/{self.config.board_id}/cards'
        self.trello_cards_url = f'{self.trello_base_url}/cards'
        self.auth_params = { 'key': self.config.api_key, 'token': self.config.api_token }

    def get_status(self, list_id):
        if list_id == self.config.todo_list_id:
            return Status.TO_DO
        elif list_id == self.config.doing_list_id:
            return Status.DOING
        else:
            return Status.DONE

    def get_trello_card_url(self, id):
        return f'{self.trello_cards_url}/{id}'

    def get_items(self):
        """
        Fetches all todo list items from Trello.

        Returns:
            list: The list of items.
        """
        print(self.config.board_id)
        response = requests.request('GET', self.trello_board_url, params=self.auth_params).json()
        
        return [ToDoItem.fromTrelloCard(card, self.get_status(card['idList'])) for card in response]


    def add_item(self, title, description = ''):
        """
        Adds a new item with the specified title and optional description to Trello.

        Args:
            title: The title of the item.
            description: The description of the item
        """

        requests.request('POST', self.trello_cards_url, params={**self.auth_params, 'idList': self.config.todo_list_id, 'name': title, 'desc': description })


    def mark_as_complete(self, id):
        """
        Moves an item from the To Do list to Done.

        Args:
            id: The id of the item to mark as complete.
        """

        requests.request('PUT', self.get_trello_card_url(id), params={**self.auth_params, 'idList': self.config.done_list_id })


    def remove_item(self, id):
        """
        Removes an existing item from Trello. 

        Args:
            id: The id of the item to remove.
        """

        requests.request('DELETE', self.get_trello_card_url(id), params=self.auth_params)

    def create_trello_board(self, name):
        response = requests.request('POST', f'{self.trello_base_url}/boards', params={**self.auth_params, 'name': name }).json()
        return response['id']

    def delete_trello_board(self, id):
        requests.request('DELETE', f'{self.trello_base_url}/boards/{id}', params=self.auth_params)