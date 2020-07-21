import pytest
from view_model import ViewModel
from to_do_item import ToDoItem, Status

@pytest.fixture
def items_view_model():
    return ViewModel([
    ToDoItem(1, "Title 1", Status.TO_DO, "Description 1"),
    ToDoItem(2, "Title 2", Status.TO_DO, "Description 2"),
    ToDoItem(3, "Title 3", Status.DOING, "Description 3"),
    ToDoItem(4, "Title 4", Status.DONE, "Description 4")
    ])

def test_return_all_items(items_view_model):
    all_items = items_view_model.items
    assert len(all_items) == 4
    assert all_items[0].id == 1

def test_return_to_do_items(items_view_model):
    to_do_items = items_view_model.to_do_items
    assert len(to_do_items) == 2
    assert to_do_items[0].id == 1
    assert to_do_items[1].id == 2

def test_return_doing_items(items_view_model):
    doing_items = items_view_model.doing_items
    assert len(doing_items) == 1
    assert doing_items[0].id == 3

def test_return_done_items(items_view_model):
    done_items = items_view_model.done_items
    assert len(done_items) == 1
    assert done_items[0].id == 4