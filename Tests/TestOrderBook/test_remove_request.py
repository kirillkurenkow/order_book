import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook import (
    RequestWasNotFoundError,
    RequestTypeError,
)
from Tests.OrderBook.Requests import (
    RequestTypes,
    AskRequest,
    BidRequest,
)
from Tests.Source import (
    Defaults,
    attach_dict_to_report,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
@pytest.mark.parametrize('request_type', [AskRequest, BidRequest])
def test_remove_request(order_book, request_type):
    """
    Test checks the possibility of removing a request from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Remove request
            E: The function is executed without any exceptions
    """
    with step('Generate request'):
        request = request_type(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Remove request'):
        order_book.delete_request(request.id)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_remove_not_existing_request(order_book):
    """
    Test checks the possibility of removing a not existing request from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Remove request
            E: RequestWasNotFoundError raised
    """
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Remove request'):
        order_book.delete_request(request.id + 1)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_remove_request_wrong_request_type(order_book):
    """
    Test checks the possibility of removing a request with wrong type from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Remove request
            E: RequestWasNotFoundError raised
    """
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Remove request'):
        order_book.delete_request(request.id, request_type=RequestTypes.BID)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestTypeError, strict=True)
def test_remove_not_existing_request_type(order_book):
    """
    Test checks the possibility of removing a request with a non-existent type from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Remove request
            E: RequestTypeError raised
    """
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Remove request'):
        order_book.delete_request(request.id, request_type='WrongRequestType')
