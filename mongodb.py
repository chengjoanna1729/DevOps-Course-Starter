import os
import pymongo
from bson import ObjectId
from datetime import datetime
from to_do_item import ToDoItem, Status

class MongoDB:
    def __init__(self):
        self.mongo_db_user = os.getenv("MONGO_DB_USER")
        self.mongo_db_password = os.getenv("MONGO_DB_PASSWORD")
        self.mongo_db_hostname = os.getenv("MONGO_DB_HOSTNAME")
        self.connection_string = f'mongodb+srv://{self.mongo_db_user}:{self.mongo_db_password}@{self.mongo_db_hostname}/todos?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(self.connection_string)
        self.db_name = os.getenv("MONGO_DB_NAME")
        self.collection = self.get_collection()

    def get_collection(self):
        return self.client[self.db_name]['all_todos']

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