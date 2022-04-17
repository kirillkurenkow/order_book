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
from Tests.Source.Schema import (
    OrderBookSchema,
    validate,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_get_snapshot(order_book):
    """
    Test checks the possibility of getting a snapshot from the OrderBook

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
        3. Get snapshot
            E: Snapshot received successfully
        4. Validate snapshot
            E: Validation succeeded
    """
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
        validate(snapshot, OrderBookSchema.snapshot)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_get_empty_snapshot(order_book):
    """
    Test checks the possibility of getting an empty snapshot from the OrderBook

    Steps:
        1. Get snapshot
            E: Snapshot received successfully
        2. Validate snapshot
            E: Validation succeeded
    """
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Validate snapshot'):
        validate(snapshot, OrderBookSchema.snapshot)


@severity(severity_level.CRITICAL)
@pytest.mark.positive
def test_change_snapshot(order_book):
    """
    Test checks the possibility of changing a snapshot dict object from the OrderBook

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
        3. Get snapshot
            E: Snapshot received successfully
        4. Change snapshot
            E: Snapshot dict object changed
        5. Get snapshot
            E: Snapshot received successfully
        6. Check snapshot not changed
            E: Snapshot is the same as in the step 3
    """
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
