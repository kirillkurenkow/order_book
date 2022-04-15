from typing import (
    Dict,
    List,
)

from . import (
    RequestWasNotFoundError,
    RequestIdError,
    RequestError,
    RequestTypeError,
    RequestAlreadyExistsError,
)
from .Requests import (
    Request,
    RequestTypes,
    PRICE_TYPE,
)

__all__ = ['OrderBook']

_REQUESTS_LIST_TYPE = Dict[str, List[Request]]


class OrderBook:
    def __init__(self):
        self._requests: _REQUESTS_LIST_TYPE = {
            RequestTypes.ASK: [],
            RequestTypes.BID: [],
        }

    @staticmethod
    def __check_request_id(request_id: int) -> None:
        if not isinstance(request_id, int):
            raise RequestIdError(f'request_id should be instance of int: {request_id}') from TypeError
        if request_id < 0:
            raise RequestIdError(f'request_id can not be lower than 0: {request_id}') from ValueError

    @staticmethod
    def __check_request_type(request_type: str) -> None:
        if request_type not in [RequestTypes.ASK, RequestTypes.BID]:
            raise RequestTypeError(
                f'Request type should be {RequestTypes.ASK} or {RequestTypes.BID}: {request_type}'
            ) from TypeError

    def add_request(self, request: Request) -> None:
        if not isinstance(request, Request):
            raise RequestError(f'Request should be instance of Request: {request}.') from TypeError
        if request in self._requests[request.type]:
            raise RequestAlreadyExistsError(f'Request already exists: {request}.')
        if self._get_request(request.id, raise_if_not_found=False) is not None:
            raise RequestAlreadyExistsError(f'Request with id "{request.id}" already exists.')
        self._requests[request.type].append(request)

    def delete_request(self, request_id: int, request_type: str = None) -> None:
        request = self._get_request(request_id=request_id, request_type=request_type)
        self._requests[request.type].remove(request)

    def _get_request(self, request_id: int, request_type: str = None, raise_if_not_found: bool = True) -> Request:
        self.__check_request_id(request_id)
        if request_type is None:
            for request in [request for request_type, request_list in self._requests.items() for request in
                            request_list]:
                if request.id == request_id:
                    return request
        else:
            self.__check_request_type(request_type)
            for request in self._requests[request_type]:
                if request_id == request:
                    return request
        if raise_if_not_found:
            raise RequestWasNotFoundError(f'Request with id "{request_id}" was not found.')

    def get_request_info(self, request_id: int, request_type: str = None) -> str:
        return str(self._get_request(request_id=request_id, request_type=request_type))

    def change_request_info(self, request_id: int, price: PRICE_TYPE = None, volume: int = None) -> None:
        if not any([x is not None for x in (price, volume)]):
            raise ValueError('At least one of arguments should be provided: price, volume.')
        request = self._get_request(request_id)
        if price is not None:
            request.price = price
        if volume is not None:
            request.volume = volume

    def get_snapshot(self) -> _REQUESTS_LIST_TYPE:
        result = self._requests.copy()
        result = {
            'Asks': result[RequestTypes.ASK],
            'Bids': result[RequestTypes.BID],
        }
        return result
