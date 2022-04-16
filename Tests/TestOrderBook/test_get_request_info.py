import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from OrderBook import (
    RequestWasNotFoundError,
    RequestTypeError,
)
from OrderBook.Requests import (
    AskRequest,
    BidRequest,
    RequestTypes,
)
from Tests.Source import (
    Defaults,
    attach_dict_to_report,
    compare_request_with_request_info,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
@pytest.mark.parametrize('request_type', [AskRequest, BidRequest])
def test_get_request_info(order_book, request_type):
    with step('Generate request'):
        request = request_type(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get request info'):
        request_info = order_book.get_request_info(request.id)
        attach_dict_to_report(request_info, 'Request info')
        compare_request_with_request_info(request, request_info)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_get_not_existing_request_info(order_book):
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get request info'):
        order_book.get_request_info(request.id + 1)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_get_not_existing_request_type_info(order_book):
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
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Get request info'):
        order_book.get_request_info(request.id, request_type='SomeWrongType')
