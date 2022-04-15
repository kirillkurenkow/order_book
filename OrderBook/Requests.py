from typing import Union

from . import (
    RequestPriceError,
    RequestVolumeError,
)

__all__ = ['RequestTypes', 'Request', 'AskRequest', 'BidRequest', 'PRICE_TYPE']

PRICE_TYPE = Union[int, float]


class RequestTypes:
    ASK = 'Ask'
    BID = 'Bid'


class Request:
    _curr_id: int = 0

    def __init__(self, price: PRICE_TYPE, volume: int):
        self._price: PRICE_TYPE = ...
        self._volume: int = ...
        self.price = price
        self.volume = volume
        self._id: int = self._curr_id
        Request._curr_id += 1

    @property
    def price(self) -> PRICE_TYPE:
        return self._price

    @price.setter
    def price(self, value: PRICE_TYPE) -> None:
        if not isinstance(value, PRICE_TYPE):
            raise RequestPriceError(f'Price should be instance of int or float: {value}.') from TypeError
        if value <= 0:
            raise RequestPriceError('Price should be over than 0.') from ValueError
        self._price = value

    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, value) -> None:
        if not isinstance(value, int):
            raise RequestVolumeError(f'Volume should be instance of int: {value}.') from TypeError
        if value < 1:
            raise RequestVolumeError('Volume can not be lower than 1.') from ValueError
        self._volume = value

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> str:
        return ''

    def __str__(self) -> str:
        result = {
            'id': self.id,
            'price': self.price,
            'volume': self.volume,
            'type': self.type,
        }
        return str(result)


class AskRequest(Request):
    @property
    def type(self) -> str:
        return RequestTypes.ASK


class BidRequest(Request):
    @property
    def type(self) -> str:
        return RequestTypes.BID
