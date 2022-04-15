import logging
from typing import (
    Dict,
    List,
    Optional,
    Union,
    Tuple,
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

LOGGER = logging.getLogger(__name__)
_REQUESTS_LIST_TYPE = Dict[str, List[Request]]


class OrderBook:
    """
    Object for working with a list of requests
    """

    def __init__(self):
        self._requests: _REQUESTS_LIST_TYPE = {
            RequestTypes.ASK: [],
            RequestTypes.BID: [],
        }

    @staticmethod
    def __check_request_id(request_id: int) -> None:
        """
        request_id validation method

        :param request_id: Request id

        :return: None
        """
        # request_id should be an instance of int
        if not isinstance(request_id, int):
            LOGGER.error('request_id is not instance if int (%s)' % type(request_id))
            raise RequestIdError(f'request_id should be instance of int: {request_id}') from TypeError

        # request_id can not be lower than 0
        if request_id < 0:
            LOGGER.error('request_id is lower than 0 (%s)' % request_id)
            raise RequestIdError(f'request_id can not be lower than 0: {request_id}') from ValueError

    @staticmethod
    def __check_request_type(request_type: str) -> None:
        """
        request_type validation method

        :param request_type: Request type

        :return: None
        """
        # request_type should be Ask or Bid
        if request_type not in [RequestTypes.ASK, RequestTypes.BID]:
            LOGGER.error('request_type is not Ask or Bid (%s)' % request_type)
            raise RequestTypeError(
                f'The request type should be {RequestTypes.ASK} or {RequestTypes.BID}: {request_type}'
            ) from TypeError

    def add_request(self, request: Request) -> None:
        """
        Method for adding a new request to the requests list

        :param request: Request object

        :return: None
        """
        LOGGER.debug('Trying to add a new request: %s' % str(request))

        # The request must be an instance of the Request
        if not isinstance(request, Request):
            LOGGER.error('The request is not an instance of the Request (%s)' % type(request))
            raise RequestError(f'The request must be an instance of the Request: {request}.') from TypeError

        # The request must not exist in the requests list
        if request in self._requests[request.type]:
            LOGGER.warning('The request is already exists')
            raise RequestAlreadyExistsError(f'The request is already exists: {request}.')

        # The request with the same id must not exist in the requests list
        if self._get_request(request.id, raise_if_not_found=False) is not None:
            LOGGER.error('The request with id "%s" is already exists' % request.id)
            raise RequestAlreadyExistsError(f'The request with id "{request.id}" is already exists.')

        # Adding the request to the requests list
        self._requests[request.type].append(request)

        LOGGER.debug('The request was added successfully')

    def add_requests(self, requests: List[Request],
                     raise_exceptions: bool = True) -> Union[List[Tuple[Request, str]], None]:
        """
        Method for adding multiple requests to the requests list
        If raise_exceptions is False method will return a list of "bad" requests

        :param requests: List of requests
        :param raise_exceptions: Raise exceptions or not
        :return: List of "bad" requests or None
        """
        bad_requests = []
        for request in requests:
            try:
                self.add_request(request)
            except Exception as exception:
                if raise_exceptions:
                    raise exception
                bad_requests.append((request, type(exception).__name__))
                continue
        return bad_requests

    def delete_request(self, request_id: int, request_type: Optional[str] = None) -> None:
        """
        Method for deleting a request from the requests list

        :param request_id: Request id
        :param request_type: Request type

        :return: None
        """
        LOGGER.debug('Trying to delete the request with id "%s" and type "%s"' % (request_id, request_type))

        # Searching request
        request = self._get_request(request_id=request_id, request_type=request_type)

        # Deleting request
        self._requests[request.type].remove(request)

        LOGGER.debug('The request was deleted successfully')

    def _get_request(self, request_id: int, request_type: Optional[str] = None,
                     raise_if_not_found: Optional[bool] = True) -> Request:
        """
        Method for getting a request object from the requests list

        :param request_id: Request id
        :param request_type: Request type
        :param raise_if_not_found: Raise RequestWasNotFoundError exception if request was not found or not

        :return: Request object
        """
        LOGGER.debug('Trying to find the request with id "%s"' % request_id)
        self.__check_request_id(request_id)

        # If request_type is None - creating a list self._requests['Ask'] + self._requests['Bid']
        if request_type is None:
            requests_list = self._requests[RequestTypes.ASK] + self._requests[RequestTypes.BID]
        # Else searching in self._requests[request_type]
        else:
            self.__check_request_type(request_type)
            requests_list = self._requests[request_type]

        # Searching request
        for request in requests_list:
            if request_id == request.id:
                LOGGER.debug('The request was found successfully')
                return request

        LOGGER.warning('The request with id "%s" was not found' % request_id)

        # Raising exception if request was not found and raise_if_not_found is True
        if raise_if_not_found:
            raise RequestWasNotFoundError(f'The request with id "{request_id}" was not found.')

    def get_request_info(self, request_id: int, request_type: Optional[str] = None) -> dict:
        """
        Method for getting a request info from the requests list

        :param request_id: Request id
        :param request_type: Request type

        :return: A dict with request info
        """
        return self._get_request(request_id=request_id, request_type=request_type).as_dict

    def change_request_info(self, request_id: int, price: Optional[PRICE_TYPE] = None,
                            volume: Optional[int] = None) -> None:
        """
        Method for changing a request info in the requests list

        :param request_id: Request id
        :param price: New price
        :param volume: New volume

        :return: None
        """
        LOGGER.debug('Trying to change the request info (request_id: %s)' % request_id)

        # Either price or volume should be specified
        if not any([x is not None for x in (price, volume)]):
            LOGGER.error('None of price or volume were specified')
            raise ValueError('Either price or volume should be specified')

        # Searching request
        request = self._get_request(request_id)

        # Changing data
        if price is not None:
            LOGGER.debug('Changing price from %s to %s' % (request.price, price))
            request.price = price
        if volume is not None:
            LOGGER.debug('Changing volume from %s to %s' % (request.volume, volume))
            request.volume = volume

        LOGGER.debug('The request info was changed successfully')

    def get_snapshot(self) -> dict:
        """
        Method for getting a snapshot of the current requests list

        :return: Requests dict: {'Asks': [...], 'Bids': [...]}
        """
        # Creating a copy to avoid changing of the self._requests dict
        result = self._requests.copy()

        # Changing keys to follow the documentation
        result = {
            'Asks': [x.as_dict for x in result[RequestTypes.ASK]],
            'Bids': [x.as_dict for x in result[RequestTypes.BID]],
        }
        LOGGER.debug('A new snapshot was created: %s' % result)
        return result
