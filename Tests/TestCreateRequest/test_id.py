import pytest
from allure import (
    step,
    severity,
    severity_level,
)

from Tests.OrderBook.Requests import Request
from Tests.Source import (
    attach_dict_to_report,
    Defaults,
)


@severity(severity_level.BLOCKER)
@pytest.mark.positive
def test_id_order():
    with step('Creating 5 requests'):
        requests = [Request(price=Defaults.price, volume=Defaults.volume) for _ in range(5)]
        base_id = requests[0].id
        for i, request in enumerate(requests):
            attach_dict_to_report(request.as_dict, name=f'Request {i + 1}')
            assert request.id == base_id
            base_id += 1
