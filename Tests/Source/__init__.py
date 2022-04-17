import json
from typing import Union

import allure

from Tests.OrderBook.Requests import Request

from .ConfigReader import Config


def attach_dict_to_report(data: Union[list, dict], name: str) -> None:
    """
    Attach dict to allure report

    :param data: Dict or list to attach
    :param name: Attachment name

    :return: None
    """
    data = json.dumps(data, ensure_ascii=False, indent=4)
    allure.attach(data, name=name, attachment_type=allure.attachment_type.JSON)


def compare_request_with_request_info(request: Request, request_info: dict) -> None:
    """
    Compare request object with request_info received from OrderBook.get_request_info method

    :param request: Request object
    :param request_info: request_info dict

    :return: None
    """
    assert request.price == request_info['price'], 'Wrong price in request_info'
    assert request.volume == request_info['volume'], 'Wrong volume in request_info'
    assert request.type == request_info['type'], 'Wrong type in request_info'
    assert request.id == request_info['id'], 'Wrong id in request_info'


def check_request_not_in_snapshot(request: Request, snapshot: dict) -> None:
    """
    Check that snapshot has no request_info with request.id

    :param request: Request object
    :param snapshot: Snapshot dict

    :return: None
    """
    all_requests = snapshot['Asks'] + snapshot['Bids']
    for snapshot_request in all_requests:
        assert snapshot_request['id'] != request.id, 'Request with the same id was found in the snapshot'


class Defaults:
    """
    Class with default test values
    """
    __config = Config('defaults.cfg')

    __REQUEST_SECTION = 'REQUEST'
    price = __config.getnumber(__REQUEST_SECTION, 'price')
    volume = __config.getnumber(__REQUEST_SECTION, 'volume')
