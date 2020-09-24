import pytest
from datetime import datetime, timedelta

from view_model import ViewModel
from to_do_item import ToDoItem, Status

@pytest.fixture
def items_view_model():
    return ViewModel([
    ToDoItem(1, "Title 1", Status.TO_DO, "Description 1", datetime.now()),
    ToDoItem(2, "Title 2", Status.TO_DO, "Description 2", datetime.now()),
    ToDoItem(3, "Title 3", Status.DOING, "Description 3", datetime.now()),
    ToDoItem(4, "Title 4", Status.DONE, "Description 4", datetime.now())
    ])

    
@pytest.fixture
def done_items_view_model():
    return ViewModel([
        ToDoItem(11, "Title 1", Status.DONE, "3 days done", datetime.now() - timedelta(days=3)),
        ToDoItem(12, "Title 2", Status.DONE, "2 hours done", datetime.now() - timedelta(hours=2)),
        ToDoItem(13, "Title 3", Status.DONE, "Just done", datetime.now()),
        ToDoItem(14, "Title 4", Status.DONE, "30 days done", datetime.now() - timedelta(days=30)),
        ToDoItem(15, "Title 5", Status.DONE, "23 hours done", datetime.now() - timedelta(hours=23))
    ])

def test_return_all_items(items_view_model):
    all_items = items_view_model.items
    assert len(all_items) == 4
    assert all_items[0].id == 1

def test_return_to_do_items(items_view_model):
    to_do_items = items_view_model.to_do_items
    assert len(to_do_items) == 2
    assert all(item.id in (1, 2) for item in to_do_items)

def test_return_doing_items(items_view_model):
    doing_items = items_view_model.doing_items
    assert len(doing_items) == 1
    assert doing_items[0].id == 3

def test_return_done_items(items_view_model):
    done_items = items_view_model.done_items
    assert len(done_items) == 1
    assert done_items[0].id == 4

def test_show_all_done_items_true(items_view_model):
    assert items_view_model.show_all_done_items is True

def test_show_all_done_items_false(done_items_view_model):
    assert done_items_view_model.show_all_done_items is False

def test_return_recent_done_items(done_items_view_model):
    recent_done_items = done_items_view_model.recent_done_items
    assert len(recent_done_items) == 3
    assert all(item.id in (12, 13, 15) for item in recent_done_items)

def test_return_older_done_items(done_items_view_model):
    older_done_items = done_items_view_model.older_done_items
    assert len(older_done_items) == 2    
    assert all(item.id in (11, 14) for item in older_done_items)
