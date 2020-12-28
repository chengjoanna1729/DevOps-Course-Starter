import os
from to_do_item import ToDoItem, Status
import requests

class Trello:
    def __init__(self):
        self.board_id = os.getenv("TRELLO_BOARD_ID")
        self.trello_base_url = 'https://api.trello.com/1'
        self.trello_board_url = f'{self.trello_base_url}/boards/{self.board_id}/cards'
        self.trello_cards_url = f'{self.trello_base_url}/cards'
        self.auth_params = { 'key': os.getenv("TRELLO_API_KEY"), 'token': os.getenv("TRELLO_API_TOKEN") }

        lists = self.get_lists()
        self.todo_list_id = next(list for list in lists if list['name'] == "To Do")['id']
        self.doing_list_id = next(list for list in lists if list['name'] == "Doing")['id']
        self.done_list_id = next(list for list in lists if list['name'] == "Done")['id']

    def get_status(self, list_id):
        if list_id == self.todo_list_id:
            return Status.TO_DO
        elif list_id == self.doing_list_id:
            return Status.DOING
        else:
            return Status.DONE

    def get_trello_card_url(self, id):
        return f'{self.trello_cards_url}/{id}'

    def get_lists(self):
        return requests.request('GET', f'{self.trello_base_url}/boards/{self.board_id}/lists', params=self.auth_params).json()

    def get_items(self):
        """
        Fetches all todo list items from Trello.

        Returns:
            list: The list of items.
        """
        response = requests.request('GET', self.trello_board_url, params=self.auth_params).json()
        
        return [ToDoItem.fromTrelloCard(card, self.get_status(card['idList'])) for card in response]


    def add_item(self, title, description = ''):
        """
        Adds a new item with the specified title and optional description to Trello.

        Args:
            title: The title of the item.
            description: The description of the item
        """

        requests.request('POST', self.trello_cards_url, params={**self.auth_params, 'idList': self.todo_list_id, 'name': title, 'desc': description })


    def mark_as_complete(self, id):
        """
        Moves an item from the To Do list to Done.

        Args:
            id: The id of the item to mark as complete.
        """

        requests.request('PUT', self.get_trello_card_url(id), params={**self.auth_params, 'idList': self.done_list_id })


    def remove_item(self, id):
        """
        Removes an existing item from Trello. 

        Args:
            id: The id of the item to remove.
        """

        requests.request('DELETE', self.get_trello_card_url(id), params=self.auth_params)

    def create_trello_board(self, name):
        board_id = requests.request('POST', f'{self.trello_base_url}/boards', params={**self.auth_params, 'name': name }).json()['id']
        requests.request('POST', f'{self.trello_base_url}/boards/{id}/lists', params={**self.auth_params, 'name': 'To Do' })
        requests.request('POST', f'{self.trello_base_url}/boards/{id}/lists', params={**self.auth_params, 'name': 'Doing' })
        requests.request('POST', f'{self.trello_base_url}/boards/{id}/lists', params={**self.auth_params, 'name': 'Done' })
        return board_id

    def delete_trello_board(self, id):
        requests.request('DELETE', f'{self.trello_base_url}/boards/{id}', params=self.auth_params)