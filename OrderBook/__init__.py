__all__ = [
    # Exceptions
    'RequestError',
    'RequestIdError',
    'RequestPriceError',
    'RequestVolumeError',
    'RequestTypeError',
    'RequestWasNotFoundError',
]


class RequestError(Exception):
    ...


class RequestIdError(RequestError):
    ...


class RequestPriceError(RequestError):
    ...


class RequestVolumeError(RequestError):
    ...


class RequestTypeError(RequestError):
    ...


class RequestWasNotFoundError(RequestError):
    ...


class RequestAlreadyExistsError(RequestError):
    ...
