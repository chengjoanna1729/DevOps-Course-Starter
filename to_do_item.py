from enum import Enum
from datetime import datetime

def parse_trello_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

class Status(Enum):
    TO_DO = "To Do"
    DOING = "Doing"
    DONE = "Done"

class ToDoItem:
    def __init__(self, id, title, status, description, last_modified):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.last_modified = last_modified

    @classmethod
    def fromTrelloCard(cls, card, status):
        return cls(card['id'], card['name'], status, card['desc'], parse_trello_date(card['dateLastActivity']))
        