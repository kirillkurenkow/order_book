import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook import RequestPriceError
from Tests.OrderBook.Requests import Request
from Tests.Source import (
    attach_dict_to_report,
    Defaults,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_price_int():
    """
    Test checks the possibility of creating a request with a price of type int

    Steps:
        1. Creating request
            E: Request created successfully
    """
    with step('Creating request'):
        request = Request(price=100, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_price_float():
    """
    Test checks the possibility of creating a request with a price of type float

    Steps:
        1. Creating request
            E: Request created successfully
    """
    with step('Creating request'):
        request = Request(price=100.5, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError, strict=True)
def test_negative_price():
    """
    Test checks the possibility of creating a request with a price of a negative value

    Steps:
        1. Creating request
            E: Request not created
            E: RequestPriceError raised
    """
    with step('Creating request'):
        Request(price=-100, volume=Defaults.volume)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError, strict=True)
def test_zero_price():
    """
    Test checks the possibility of creating a request with a price of zero value

    Steps:
        1. Creating request
            E: Request not created
            E: RequestPriceError raised
    """
    with step('Creating request'):
        Request(price=0, volume=Defaults.volume)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError, strict=True)
@pytest.mark.parametrize('price', [
    f'{Defaults.price}',
    [Defaults.price],
    {Defaults.price},
    None,
])
def test_wrong_price_type(price):
    """
    Test checks the possibility of creating a request with a price of the wrong type

    Steps:
        1. Creating request
            E: Request not created
            E: RequestPriceError raised
    """
    with step('Creating request'):
        Request(price=price, volume=Defaults.volume)  # noqa
