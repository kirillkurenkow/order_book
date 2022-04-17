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
    AskRequest,
    BidRequest,
    RequestTypes,
)
from Tests.Source import (
    Defaults,
    attach_dict_to_report,
    compare_request_with_request_info,
)
from Tests.Source.Schema import (
    OrderBookSchema,
    validate,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
@pytest.mark.parametrize('request_type', [AskRequest, BidRequest])
def test_get_request_info(order_book, request_type):
    """
    Test checks the possibility of getting a request info from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Get request info
            E: Request info received successfully
        4. Validate request info
            E: Validation succeeded
    """
    with step('Generate request'):
        request = request_type(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get request info'):
        request_info = order_book.get_request_info(request.id)
        attach_dict_to_report(request_info, 'Request info')
        compare_request_with_request_info(request, request_info)
    with step('Validate request info'):
        validate(request_info, OrderBookSchema.request_info)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_get_not_existing_request_info(order_book):
    """
    Test checks the possibility of getting a not existing request info from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Get not existing request info
            E: RequestWasNotFoundError raised
    """
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get not existing request info'):
        order_book.get_request_info(request.id + 1)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_get_not_existing_request_type_info(order_book):
    """
    Test checks the possibility of getting a request info with a wrong request type from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Get request info
            E: RequestWasNotFoundError raised
    """
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get request info'):
        order_book.get_request_info(request.id, request_type=RequestTypes.BID)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestTypeError, strict=True)
def test_get_request_info_wrong_request_type(order_book):
    """
    Test checks the possibility of getting a request info with a not existing request type from the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Get request info
            E: RequestTypeError raised
    """
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get request info'):
        order_book.get_request_info(request.id, request_type='SomeWrongType')
