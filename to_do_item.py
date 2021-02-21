from enum import Enum
from datetime import datetime

def parse_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

class Status(Enum):
    TO_DO = "To Do"
    DOING = "Doing"
    DONE = "Done"

class ToDoItem:
    def __init__(self, id, title, status, last_modified):
        self.id = id
        self.title = title
        self.status = status
        self.last_modified = last_modified

    @classmethod
    def fromJson(cls, item):
        return cls(str(item['_id']), item['name'], Status(item['status']), parse_date(item['dateLastActivity']))
        