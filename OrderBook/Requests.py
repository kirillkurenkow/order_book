import logging
from typing import Union

from . import (
    RequestPriceError,
    RequestVolumeError,
)

__all__ = ['RequestTypes', 'Request', 'AskRequest', 'BidRequest', 'PRICE_TYPE']

PRICE_TYPE = Union[int, float]
LOGGER = logging.getLogger(__name__)


class RequestTypes:
    """
    Request types
    """
    ASK = 'Ask'
    BID = 'Bid'


class Request:
    """
    Base request without type
    """
    _curr_id: int = 0

    def __init__(self, price: PRICE_TYPE, volume: int):
        """
        :param price: Request price
        :param volume: Request volume
        """
        self._price: PRICE_TYPE = ...
        self._volume: int = ...
        self.price = price
        self.volume = volume
        self._id: int = self._curr_id
        Request._curr_id += 1
        LOGGER.debug('New request was created: %s' % str(self))

    @property
    def price(self) -> PRICE_TYPE:
        """
        Request price getter

        :return: Request price
        """
        return self._price

    @price.setter
    def price(self, value: PRICE_TYPE) -> None:
        """
        Request price setter

        :param value: New request price

        :return: None
        """
        LOGGER.debug(f'Trying to set new price (%s) for request with id "%s"' % (value, self.id))

        # Price should be instance of int or float
        if not isinstance(value, PRICE_TYPE):
            LOGGER.error('The new price is not an int or float instance (%s)' % type(value))
            raise RequestPriceError(f'Price should be instance of int or float: {value}.') from TypeError

        # Price should be over than 0
        if value <= 0:
            LOGGER.error('The new price is lower than 0 (%s)' % value)
            raise RequestPriceError('Price should be over than 0.') from ValueError

        LOGGER.debug('New price was set successfully')
        self._price = value

    @property
    def volume(self) -> int:
        """
        Request volume getter

        :return: Request volume
        """
        return self._volume

    @volume.setter
    def volume(self, value) -> None:
        """
        Request volume setter

        :param value: New request volume

        :return: None
        """
        LOGGER.debug(f'Trying to set new volume (%s) for request with id "%s"' % (value, self.id))

        # Volume should be instance of int
        if not isinstance(value, int):
            LOGGER.error('The new volume is not an int instance (%s)' % type(value))
            raise RequestVolumeError(f'Volume should be instance of int: {value}.') from TypeError

        # Volume can not be lower than 1
        if value < 1:
            LOGGER.error('The new volume is lower than 1 (%s)' % value)
            raise RequestVolumeError('Volume can not be lower than 1.') from ValueError
        self._volume = value

    @property
    def id(self) -> int:
        """
        Request id getter

        :return: Request id
        """
        return self._id

    @property
    def type(self) -> str:
        """
        Request type getter

        :return: ''
        """
        return ''

    def __str__(self) -> str:
        """
        Request string representation

        :return: str: '{'id': ..., 'price': ..., 'volume': ..., 'type': ...}'
        """
        result = {
            'id': self.id,
            'price': self.price,
            'volume': self.volume,
            'type': self.type,
        }
        return str(result)


class AskRequest(Request):
    """
    Request of type 'Ask'
    """

    @property
    def type(self) -> str:
        """
        Overrides Request.type

        :return: 'Ask'
        """
        return RequestTypes.ASK


class BidRequest(Request):
    """
    Request of type 'Bid'
    """

    @property
    def type(self) -> str:
        """
        Overrides Request.type

        :return: 'Bid'
        """
        return RequestTypes.BID
