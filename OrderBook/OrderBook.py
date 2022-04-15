from typing import (
    Dict,
    List,
    Optional,
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
    """
    Object for working with list of requests
    """

    def __init__(self):
        self._requests: _REQUESTS_LIST_TYPE = {
            RequestTypes.ASK: [],
            RequestTypes.BID: [],
        }

    @staticmethod
    def __check_request_id(request_id: int) -> None:
        """
        Method for validating request_id

        :param request_id: Request id

        :return: None
        """
        if not isinstance(request_id, int):
            raise RequestIdError(f'request_id should be instance of int: {request_id}') from TypeError
        if request_id < 0:
            raise RequestIdError(f'request_id can not be lower than 0: {request_id}') from ValueError

    @staticmethod
    def __check_request_type(request_type: str) -> None:
        """
        Method for validation request_type

        :param request_type: Request type

        :return: None
        """
        if request_type not in [RequestTypes.ASK, RequestTypes.BID]:
            raise RequestTypeError(
                f'Request type should be {RequestTypes.ASK} or {RequestTypes.BID}: {request_type}'
            ) from TypeError

    def add_request(self, request: Request) -> None:
        """
        Method for adding new request to requests list

        :param request: Request object

        :return: None
        """
        # Request should be instance of Request
        if not isinstance(request, Request):
            raise RequestError(f'Request should be instance of Request: {request}.') from TypeError

        # Request should not exist in list
        if request in self._requests[request.type]:
            raise RequestAlreadyExistsError(f'Request already exists: {request}.')

        # Request with the same id should not exist
        if self._get_request(request.id, raise_if_not_found=False) is not None:
            raise RequestAlreadyExistsError(f'Request with id "{request.id}" already exists.')

        # Adding request to list
        self._requests[request.type].append(request)

    def delete_request(self, request_id: int, request_type: Optional[str] = None) -> None:
        """
        Method for deleting request from requests list

        :param request_id: Request id
        :param request_type: Request type

        :return: None
        """
        # Searching request
        request = self._get_request(request_id=request_id, request_type=request_type)

        # Deleting request
        self._requests[request.type].remove(request)

    def _get_request(self, request_id: int, request_type: Optional[str] = None,
                     raise_if_not_found: Optional[bool] = True) -> Request:
        """
        Method for getting request object from requests list

        :param request_id: Request id
        :param request_type: Request type
        :param raise_if_not_found: Raise RequestWasNotFoundError exception if request was not found or not

        :return: Request object
        """
        self.__check_request_id(request_id)

        # If request_type is None - creating list self._requests['Ask'] + self._requests['Bid']
        if request_type is None:
            requests_list = [request for request_type, request_list in self._requests.items() for request in
                             request_list]
        # Else searching in self._requests[request_type]
        else:
            self.__check_request_type(request_type)
            requests_list = self._requests[request_type]

        # Searching request
        for request in requests_list:
            if request_id == request:
                return request

        # Raising exception if request was not found and raise_if_not_found is True
        if raise_if_not_found:
            raise RequestWasNotFoundError(f'Request with id "{request_id}" was not found.')

    def get_request_info(self, request_id: int, request_type: Optional[str] = None) -> str:
        """
        Method for getting request info from requests list

        :param request_id: Request id
        :param request_type: Request type

        :return: str(Request object)
        """
        return str(self._get_request(request_id=request_id, request_type=request_type))

    def change_request_info(self, request_id: int, price: Optional[PRICE_TYPE] = None,
                            volume: Optional[int] = None) -> None:
        """
        Method for changing request info in requests list

        :param request_id: Request id
        :param price: New price
        :param volume: New volume

        :return: None
        """
        # Either price or volume should be specified
        if not any([x is not None for x in (price, volume)]):
            raise ValueError('Either price or volume should be specified')

        # Searching request
        request = self._get_request(request_id)

        # Changing data
        if price is not None:
            request.price = price
        if volume is not None:
            request.volume = volume

    def get_snapshot(self) -> _REQUESTS_LIST_TYPE:
        """
        Method for getting snapshot of current requests list

        :return: Requests dict: {'Asks': [...], 'Bids': [...]}
        """
        # Creating copy to avoid changing of self._requests dict
        result = self._requests.copy()

        # Changing keys to follow the documentation
        result = {
            'Asks': result[RequestTypes.ASK],
            'Bids': result[RequestTypes.BID],
        }
        return result
