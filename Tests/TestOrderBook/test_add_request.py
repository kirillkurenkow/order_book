from allure import step, severity, severity_level
import pytest
from OrderBook import RequestAlreadyExistsError, RequestError
from OrderBook.Requests import AskRequest, BidRequest, Request
from Tests.Source import attach_dict_to_report, Defaults, compare_request_with_request_info


@pytest.mark.positive
@severity(severity_level.BLOCKER)
@pytest.mark.parametrize('request_type', [AskRequest, BidRequest])
def test_add_request(order_book, request_type):
    with step('Generate request'):
        request = request_type(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Check request exists'):
        request_info = order_book.get_request_info(request.id)
        attach_dict_to_report(request_info, 'Request info')
        compare_request_with_request_info(request, request_info)


@pytest.mark.negative
@severity(severity_level.CRITICAL)
@pytest.mark.xfail(raises=RequestAlreadyExistsError, strict=True)
def test_add_existing_request(order_book):
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Add existing request'):
        order_book.add_request(request)


@pytest.mark.negative
@severity(severity_level.CRITICAL)
@pytest.mark.xfail(raises=RequestAlreadyExistsError, strict=True)
def test_add_request_with_existing_id(order_book):
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
        request_with_the_same_id = BidRequest(Defaults.price, Defaults.volume)
        request_with_the_same_id._id = request.id
        attach_dict_to_report(request_with_the_same_id.as_dict, 'Request with the same id')
    with step('Add request'):
        order_book.add_request(request)
    with step('Add request with the same id'):
        order_book.add_request(request_with_the_same_id)


@pytest.mark.negative
@severity(severity_level.CRITICAL)
@pytest.mark.parametrize('request_', [
    AskRequest(Defaults.price, Defaults.volume).as_dict,
    str(BidRequest(Defaults.price, Defaults.volume).as_dict),
])
@pytest.mark.xfail(raises=RequestError, strict=True)
def test_add_not_a_request(order_book, request_):
    with step('Add not a request'):
        order_book.add_request(request_)
