import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook.Requests import (
    AskRequest,
    BidRequest,
)
from Tests.Source import (
    Defaults,
    attach_dict_to_report,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_get_snapshot(order_book):
    with step('Generate requests'):
        request_ask = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_ask.as_dict, 'Request ask')
        request_bid = BidRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_bid.as_dict, 'Request bid')
    with step('Add requests'):
        order_book.add_request(request_ask)
        order_book.add_request(request_bid)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Validate snapshot'):
        # todo Add validation
        ...


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_get_empty_snapshot(order_book):
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Validate snapshot'):
        # todo Add validation
        ...


@severity(severity_level.CRITICAL)
@pytest.mark.positive
def test_change_snapshot(order_book):
    with step('Generate requests'):
        request_ask = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_ask.as_dict, 'Request ask')
        request_bid = BidRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_bid.as_dict, 'Request bid')
    with step('Add requests'):
        order_book.add_request(request_ask)
        order_book.add_request(request_bid)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Change snapshot'):
        changed_snapshot = snapshot.copy()
        for request_type, requests_list in changed_snapshot.items():
            for request in requests_list:
                request['price'] += 10
        attach_dict_to_report(changed_snapshot, 'Changed snapshot')
    with step('Get snapshot'):
        new_snapshot = order_book.get_snapshot()
        attach_dict_to_report(new_snapshot, 'New snapshot')
    with step('Check snapshot not changed'):
        assert new_snapshot != changed_snapshot, 'Snapshot has changed'
