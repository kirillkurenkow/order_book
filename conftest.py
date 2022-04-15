import pytest
import logging
from OrderBook.OrderBook import OrderBook


@pytest.fixture(scope='session', autouse=True)
def init_logging():
    logging.basicConfig(filename='tests.log', filemode='w', level=logging.DEBUG)


@pytest.fixture(scope='function')
def order_book():
    order_book = OrderBook()
    yield order_book
