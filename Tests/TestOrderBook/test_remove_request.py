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
    with step('Generate request'):
        request = request_type(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Remove request'):
        order_book.delete_request(request.id)
    with step('Get snapshot'):
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_remove_not_existing_request(order_book):
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
    with step('Generate request'):
        request = AskRequest(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Remove request'):
        order_book.delete_request(request.id, request_type='WrongRequestType')
