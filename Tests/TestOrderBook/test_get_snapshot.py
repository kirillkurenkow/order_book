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
    Test checks the possibility of getting a snapshot with multiple requests from the OrderBook

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
        3. Get snapshot
            E: Snapshot received successfully
        4. Check prices
            E: Prices are correct
        5. Validate snapshot
            E: Validation succeeded
    """
    with step('Generate requests'):
        price_diff = 10
        default_prices_count = 10
        requests = [AskRequest(Defaults.price, Defaults.volume + i) for i in range(default_prices_count)]
        requests.append(AskRequest(Defaults.price + price_diff, Defaults.volume))
    with step('Add requests'):
        order_book.add_requests(requests)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Validate snapshot'):
        validate(snapshot, OrderBookSchema.snapshot)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
@pytest.mark.parametrize('request_type, request_type_snapshot', [
    (AskRequest, 'Asks'),
    (BidRequest, 'Bids'),
])
def test_snapshot_volume_counter(order_book, request_type, request_type_snapshot):
    """
    Test checks the counter of price's volume in snapshot

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
        3. Get snapshot
            E: Snapshot received successfully
        4. Check volumes
            E: Volumes are correct
    """
    with step('Generate requests'):
        price_diff = 10
        default_prices_count = 10
        requests = [request_type(Defaults.price, Defaults.volume + i) for i in range(default_prices_count)]
        requests.append(request_type(Defaults.price + price_diff, Defaults.volume))
        attach_dict_to_report(requests, 'Requests')
    with step('Add requests'):
        order_book.add_requests(requests)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Check volumes'):
        # Error messages
        wrong_volume_error = 'Wrong volume for price {}: {}'
        price_was_not_found_error = 'Price was not found: {}'

        # Flags
        default_price_found = False
        changed_price_found = False

        for price_info in snapshot[request_type_snapshot]:
            price = price_info['price']
            volume = price_info['volume']
            # Check if volume for default price was count right
            if price == Defaults.price:
                expected_volume = sum(range(Defaults.volume, Defaults.volume + default_prices_count))
                assert volume == expected_volume, wrong_volume_error.format(price, volume)
                default_price_found = True

            # Check if volume for changed price was count right
            elif price == Defaults.price + price_diff:
                assert volume == Defaults.volume, wrong_volume_error.format(price, volume)
                changed_price_found = True

            # Raise AssertionError if another price was found
            else:
                raise AssertionError(f'Unexpected price was found: {price}')

        # Check that default and changed prices were found
        assert default_price_found, price_was_not_found_error.format(Defaults.price)
        assert changed_price_found, price_was_not_found_error.format(Defaults.price + price_diff)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_snapshot_prices_order_ask(order_book):
    """
    Test checks the ASK prices order in snapshot

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
        3. Get snapshot
            E: Snapshot received successfully
        4. Check prices order
            E: Prices are in the correct order
    """
    with step('Generate requests'):
        requests_count = 10
        requests = [AskRequest(Defaults.price + i, Defaults.volume) for i in range(requests_count)]
        attach_dict_to_report([request.as_dict for request in requests], 'Requests')
    with step('Add requests'):
        order_book.add_requests(requests)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Check prices order'):
        base_prices = sorted([request.price for request in requests], reverse=True)
        attach_dict_to_report(list(base_prices), 'Expected prices')
        real_prices = [price_info['price'] for price_info in snapshot['Asks']]
        attach_dict_to_report(real_prices, 'Real prices')
        assert base_prices == real_prices, 'Wrong prices order'


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_snapshot_prices_order_bid(order_book):
    """
        Test checks the BID prices order in snapshot

        Steps:
            1. Generate requests
                E: Requests generated successfully
            2. Add requests
                E: Requests added successfully
            3. Get snapshot
                E: Snapshot received successfully
            4. Check prices order
                E: Prices are in the correct order
        """
    with step('Generate requests'):
        requests_count = 10
        requests = [BidRequest(Defaults.price + i, Defaults.volume) for i in range(requests_count)]
        attach_dict_to_report([request.as_dict for request in requests], 'Requests')
    with step('Add requests'):
        order_book.add_requests(requests)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
    with step('Check prices order'):
        base_prices = sorted([request.price for request in requests])
        attach_dict_to_report(list(base_prices), 'Expected prices')
        real_prices = [price_info['price'] for price_info in snapshot['Bids']]
        attach_dict_to_report(list(real_prices), 'Real prices')
        assert base_prices == real_prices, 'Wrong prices order'


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
        for request_type, prices_list in changed_snapshot.items():
            for price_info in prices_list:
                price_info['price'] += 10
        attach_dict_to_report(changed_snapshot, 'Changed snapshot')
    with step('Get snapshot'):
        new_snapshot = order_book.get_snapshot()
        attach_dict_to_report(new_snapshot, 'New snapshot')
    with step('Check snapshot not changed'):
        assert new_snapshot != changed_snapshot, 'Snapshot has changed'
