from typing import Union

from . import (
    RequestPriceError,
    RequestVolumeError,
)

__all__ = ['RequestTypes', 'Request', 'AskRequest', 'BidRequest', 'PRICE_TYPE']

PRICE_TYPE = Union[int, float]


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
        if not isinstance(value, PRICE_TYPE):
            raise RequestPriceError(f'Price should be instance of int or float: {value}.') from TypeError
        if value <= 0:
            raise RequestPriceError('Price should be over than 0.') from ValueError
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
        if not isinstance(value, int):
            raise RequestVolumeError(f'Volume should be instance of int: {value}.') from TypeError
        if value < 1:
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
