import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook import RequestVolumeError
from Tests.OrderBook.Requests import Request
from Tests.Source import (
    attach_dict_to_report,
    Defaults,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_volume():
    """
    Test checks the possibility of creating a request with a volume of type int

    Steps:
        1. Creating request
            E: Request created successfully
    """
    with step('Creating request'):
        request = Request(price=Defaults.price, volume=Defaults.volume)
        attach_dict_to_report(request.as_dict, 'Request')


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestVolumeError, strict=True)
def test_negative_volume():
    """
    Test checks the possibility of creating a request with a volume of a negative value

    Steps:
        1. Creating request
            E: Request not created
            E: RequestVolumeError raised
    """
    with step('Creating request'):
        Request(price=Defaults.price, volume=-5)


@severity(severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.xfail(raises=RequestVolumeError, strict=True)
def test_zero_volume():
    """
    Test checks the possibility of creating a request with a volume of zero value

    Steps:
        1. Creating request
            E: Request not created
            E: RequestVolumeError raised
    """
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
def test_wrong_volume_type(volume):
    """
    Test checks the possibility of creating a request with a volume of the wrong type

    Steps:
        1. Creating request
            E: Request not created
            E: RequestVolumeError raised
    """
    with step('Creating request'):
        Request(price=Defaults.price, volume=volume)  # noqa
