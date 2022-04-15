from allure import step, severity, severity_level
from OrderBook.Requests import Request
from OrderBook import RequestPriceError
import pytest
from Tests.Source import attach_dict_to_report, Defaults


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_price_int():
    with step('Creating request'):
        request = Request(price=100, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_price_float():
    with step('Creating request'):
        request = Request(price=100.5, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError)
def test_negative_price():
    with step('Creating request'):
        Request(price=-100, volume=Defaults.volume)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError)
def test_zero_price():
    with step('Creating request'):
        Request(price=0, volume=Defaults.volume)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestPriceError)
@pytest.mark.parametrize('price', [
    f'{Defaults.price}',
    [Defaults.price],
    {Defaults.price},
    None,
])
def test_wrong_price_type(price):
    with step('Creating request'):
        Request(price=price, volume=Defaults.volume)  # noqa
