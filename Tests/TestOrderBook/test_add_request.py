from allure import step, severity, severity_level
import pytest
from OrderBook.Requests import AskRequest, BidRequest
from Source import attach_dict_to_report, Defaults, compare_request_with_request_info


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
        snapshot = order_book.get_snapshot()
        attach_dict_to_report(snapshot, 'Snapshot')
        request_info = order_book.get_request_info(request.id)
        attach_dict_to_report(request_info, 'Request info')
        compare_request_with_request_info(request, request_info)
