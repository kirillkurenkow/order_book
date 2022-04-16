import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from OrderBook import RequestVolumeError
from OrderBook.Requests import Request
from Tests.Source import (
    attach_dict_to_report,
    Defaults,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_volume():
    with step('Creating request'):
        request = Request(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestVolumeError, strict=True)
def test_negative_volume():
    with step('Creating request'):
        Request(price=Defaults.price, volume=-5)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestVolumeError, strict=True)
def test_zero_volume():
    with step('Creating request'):
        Request(price=Defaults.price, volume=0)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestVolumeError, strict=True)
@pytest.mark.parametrize('volume', [
    f'{Defaults.volume}',
    [Defaults.volume],
    {Defaults.volume},
    None,
    1.5,
])
def test_wrong_price_type(volume):
    with step('Creating request'):
        Request(price=Defaults.price, volume=volume)  # noqa
