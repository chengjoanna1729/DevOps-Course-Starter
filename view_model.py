from datetime import datetime, timedelta
from to_do_item import Status 

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return [item for item in self._items if item.status == Status.TO_DO]
        
    @property
    def doing_items(self):
        return [item for item in self._items if item.status == Status.DOING]
        
    @property
    def done_items(self):
        return [item for item in self._items if item.status == Status.DONE]
        
    @property
    def show_all_done_items(self):
        return len(self.done_items) < 5

    @property
    def recent_done_items(self):
        return [item for item in self.done_items if datetime.now() - timedelta(days=1) < item.last_modified]

    @property
    def older_done_items(self):
        return list(set(self.done_items) - set(self.recent_done_items))
