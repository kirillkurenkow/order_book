__all__ = [
    # Exceptions
    'RequestError',
    'RequestIdError',
    'RequestPriceError',
    'RequestVolumeError',
    'RequestTypeError',
    'RequestWasNotFoundError',
    'RequestAlreadyExistsError',
]


class RequestError(Exception):
    """
    Exception for errors related to Requests.Request object
    """
    ...


class RequestIdError(RequestError):
    """
    Exception for errors related to Requests.Request.id
    """
    ...


class RequestPriceError(RequestError):
    """
    Exception for errors related to Requests.Request.price
    """
    ...


class RequestVolumeError(RequestError):
    """
    Exception for errors related to Requests.Request.volume
    """
    ...


class RequestTypeError(RequestError):
    """
    Exception for errors related to Requests.Request.type
    """
    ...


class RequestWasNotFoundError(RequestError):
    """
    Exception for errors when Requests.Request object was not found
    """
    ...


class RequestAlreadyExistsError(RequestError):
    """
    Exception for errors when trying to add already existing Requests.Request object
    """
