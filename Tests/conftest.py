import pytest

from Tests.OrderBook.OrderBook import OrderBook
from Tests.OrderBook.Requests import Request


@pytest.fixture(scope='function')
def order_book():
    order_book = OrderBook()
    yield order_book
    Request._curr_id = 0  # Reset start request id
