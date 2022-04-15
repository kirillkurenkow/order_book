from OrderBook.Requests import Request
import allure
import json


def attach_dict_to_report(data: dict, name: str) -> None:
    data = json.dumps(data, ensure_ascii=False, indent=4)
    allure.attach(data, name=name, attachment_type=allure.attachment_type.JSON)


def compare_request_with_request_info(request: Request, request_info: dict) -> None:
    assert request.price == request_info['price'], 'Wrong price in request_info'
    assert request.volume == request_info['volume'], 'Wrong volume in request_info'
    assert request.type == request_info['type'], 'Wrong type in request_info'
    assert request.id == request_info['id'], 'Wrong id in request_info'


class Defaults:
    price = 100
    volume = 1
