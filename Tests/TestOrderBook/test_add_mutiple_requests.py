import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook import RequestAlreadyExistsError
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
@pytest.mark.parametrize('requests_type', [list, tuple, set])
def test_add_multiple_requests(order_book, requests_type):
    """
    Test checks the possibility of adding multiple requests to the OrderBook

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
    """
    with step('Generate requests'):
        requests = [
            AskRequest(price=Defaults.price, volume=Defaults.volume),
            BidRequest(price=Defaults.price, volume=Defaults.volume),
        ]
        attach_dict_to_report([request.as_dict for request in requests], 'Requests')
    with step('Add requests'):
        request_with_errors = order_book.add_requests(requests_type(requests), raise_exceptions=True)
        assert not request_with_errors, 'There are requests with errors'


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_add_multiple_requests_with_errors(order_book):
    """
    Test checks the possibility of adding multiple requests when some of them have errors to the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Generate requests
            E: Requests generated successfully
        4. Add multiple requests
            E: Requests without errors added successfully
            E: List of tuples (Request, Error) with error requests was received as a result of the function execution
    """
    with step('Generate request'):
        request_ask = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_ask.as_dict, 'Request ask')
    with step('Add request'):
        order_book.add_request(request_ask)
    with step('Generate requests'):
        requests = [
            request_ask,
            BidRequest(price=Defaults.price, volume=Defaults.volume),
        ]
        attach_dict_to_report([request.as_dict for request in requests], 'Requests')
    with step('Add multiple requests'):
        request_with_errors = order_book.add_requests(requests, raise_exceptions=False)
        attach_dict_to_report([[request.as_dict, error] for request, error in request_with_errors],
                              'Requests with error')
        assert request_with_errors, 'There are no requests with errors'
        assert request_with_errors == [(request_ask, RequestAlreadyExistsError.__name__)], 'Wrong requests with errors'


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_add_multiple_requests_all_errors(order_book):
    """
    Test checks the possibility of adding multiple requests when all of them have errors to the OrderBook

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add requests
            E: Requests added successfully
        3. Add multiple requests
            E: No requests were added
            E: List of tuples (Request, Error) with error requests was received as a result of the function execution
    """
    with step('Generate requests'):
        request_ask = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_ask.as_dict, 'Request ask')
        request_bid = BidRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request_bid.as_dict, 'Request bid')
    with step('Add requests'):
        order_book.add_request(request_ask)
        order_book.add_request(request_bid)
    with step('Add multiple requests'):
        requests_with_errors = order_book.add_requests([request_ask, request_bid], raise_exceptions=False)
        attach_dict_to_report([[request.as_dict, error] for request, error in requests_with_errors],
                              'Requests with error')
        expected_requests_with_errors = [(request, RequestAlreadyExistsError.__name__) for request in
                                         [request_ask, request_bid]]
        assert requests_with_errors, 'There are no requests with errors'
        assert requests_with_errors == expected_requests_with_errors, 'Wrong requests with errors'


@severity(severity_level.CRITICAL)
@pytest.mark.positive
def test_add_0_requests(order_book):
    """
    Test checks the possibility of adding 0 requests with add_multiple_requests function to the OrderBook

    Steps:
        1. Add multiple requests
            E: The function is executed without any exceptions
    """
    with step('Add multiple requests'):
        order_book.add_requests([])


@severity(severity_level.NORMAL)
@pytest.mark.positive
def test_added_list_not_changed(order_book):
    """
    Test checks that the list of requests has not changed during the execution of the add_multiple_requests function

    Steps:
        1. Generate requests
            E: Requests generated successfully
        2. Add multiple requests
            E: Requests added successfully
        3. Check that requests list has not changed
            E: Requests list has not changed
    """
    with step('Generate requests'):
        requests = [
            AskRequest(price=Defaults.price, volume=Defaults.volume),
            BidRequest(price=Defaults.price, volume=Defaults.volume),
        ]
        attach_dict_to_report([request.as_dict for request in requests], 'Requests')
        requests_copy = requests.copy()
    with step('Add multiple requests'):
        order_book.add_requests(requests_copy, raise_exceptions=False)
    with step('Check that requests list has not changed'):
        assert requests_copy == requests
