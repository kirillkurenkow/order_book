import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook import (
    RequestPriceError,
    RequestVolumeError,
    RequestWasNotFoundError,
)
from Tests.OrderBook.Requests import (
    AskRequest,
    BidRequest,
    RequestTypes,
)
from Tests.Source import (
    attach_dict_to_report,
    Defaults,
    compare_request_with_request_info,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
@pytest.mark.parametrize('request_type', [AskRequest, BidRequest])
@pytest.mark.parametrize('new_price, new_volume', [
    (Defaults.price + 10, Defaults.volume + 1),
    (Defaults.price - 10, Defaults.volume - 1),
    (Defaults.price + 10, None),
    (None, Defaults.volume + 1),
])
def test_change_request(order_book, request_type, new_price, new_volume):
    """
    Test checks the possibility of changing a request in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request
            E: The function is executed without any exceptions
        4. Check request changed
            E: Request changed successfully
    """
    with step('Generate request'):
        request = request_type(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id, price=new_price, volume=new_volume)
    with step('Check request changed'):
        request_info = order_book.get_request_info(request.id, request.type)
        attach_dict_to_report(request_info, 'Request info')
        compare_request_with_request_info(request, request_info)


@severity(severity_level.NORMAL)
@pytest.mark.positive
@pytest.mark.parametrize('request_type', [AskRequest, BidRequest])
def test_change_same_values(order_book, request_type):
    """
    Test checks the possibility of changing a request info to the same values in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request
            E: The function is executed without any exceptions
        4. Check request info
            E: The request info is the same as before
    """
    with step('Generate request'):
        request = request_type(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id, price=request.price, volume=request.volume)
    with step('Check request info'):
        request_info = order_book.get_request_info(request.id, request.type)
        attach_dict_to_report(request_info, 'Request info')
        compare_request_with_request_info(request, request_info)


@severity(severity_level.NORMAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_change_request_type(order_book):
    """
    Test checks the possibility of changing a request type in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request
            E: TypeError raised
    """
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id, price=Defaults.price + 10, type=RequestTypes.BID)


@severity(severity_level.NORMAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_change_request_id(order_book):
    """
    Test checks the possibility of changing a request id in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request
            E: TypeError raised
    """
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id, price=Defaults.price + 10, id=RequestTypes.BID)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError, strict=True)
@pytest.mark.parametrize('new_price', [
    0,
    -Defaults.price,
    str(Defaults.price),
])
def test_change_wrong_new_price(order_book, new_price):
    """
    Test checks the possibility of changing a request price to an incorrect value in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request
            E: RequestPriceError raised
    """
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id, price=new_price)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestVolumeError, strict=True)
@pytest.mark.parametrize('new_volume', [
    float(Defaults.volume),
    0,
    -Defaults.volume,
    str(Defaults.volume),
])
def test_change_wrong_new_volume(order_book, new_volume):
    """
    Test checks the possibility of changing a request volume to an incorrect value in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request
            E: RequestVolumeError raised
    """
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id, volume=new_volume)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestWasNotFoundError, strict=True)
def test_change_not_existing_request(order_book):
    """
    Test checks the possibility of changing a not existing request in the OrderBook

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Change request with not existing id
            E: RequestWasNotFoundError raised
    """
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id + 1, price=Defaults.price + 10)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=ValueError, strict=True)
def test_change_nothing(order_book):
    """
    Test checks the possibility of using change_request_info() function without price or volume arg

    Steps:
        1. Generate request
            E: Request generated successfully
        2. Add request
            E: Request added successfully
        3. Execute change_request_info() without price and volume args
            E: ValueError raised
    """
    with step('Generate request'):
        request = AskRequest(Defaults.price, Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')
    with step('Add request'):
        order_book.add_request(request)
    with step('Change request'):
        order_book.change_request_info(request.id)
