import os
import pymongo
from bson import ObjectId
from datetime import datetime
from to_do_item import ToDoItem, Status

class MongoDB:
    def __init__(self):
        self.connection_string = os.getenv("DB_CONNECTION_STRING")
        self.client = pymongo.MongoClient(self.connection_string)
        self.collection_name = os.getenv("COLLECTION_NAME")
        self.collection = self.get_collection()

    def get_collection(self):
        return self.client[self.collection_name]['all_todos']

    def get_collection_items(self):
        return self.collection.find()

    def get_items(self):
        """
        Fetches all todo list items from the db collection.

        Returns:
            list: The list of items.
        """
        items = self.get_collection_items()
        return [ToDoItem.fromJson(item) for item in items]


    def add_item(self, title):
        """
        Adds a new item with the specified title to the db collection.

        Args:
            title: The title of the item.
        """
        self.collection.insert_one(
            {
                "name": title,
                "status": Status.TO_DO.value,
                "dateLastActivity": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
        )

    def mark_as_complete(self, id):
        """
        Moves an item from the To Do list to Done.

        Args:
            id: The id of the item to mark as complete.
        """

        self.collection.update_one(
            {
                "_id": ObjectId(id)
            },
            {
                "$set":
                {
                    "status": Status.DONE.value,
                    "dateLastActivity": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
            }
        )

    def remove_item(self, id):
        """
        Removes an existing item from the collection. 

        Args:
            id: The id of the item to remove.
        """

        self.collection.delete_one(
            {
                "_id": ObjectId(id)
            }
        )