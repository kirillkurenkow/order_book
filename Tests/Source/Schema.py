import logging
from typing import Optional

from schema import (
    Schema,
    Or,
    SchemaError,
)

from . import attach_dict_to_report

__all__ = ['OrderBookSchema', 'validate']
LOGGER = logging.getLogger(__name__)


class OrderBookSchema:
    """
    Schemas for OrderBook
    """
    request_info = Schema({
        'id': int,
        'price': Or(int, float),
        'volume': int,
        'type': Or('Ask', 'Bid'),
    }, name='Request info')
    snapshot = Schema({
        'Asks': [request_info],
        'Bids': [request_info],
    }, name='Snapshot')


class JsonSchemaValidationError(AssertionError):
    """
    Custom exception for validation error
    Should inherit AssertionError to be product error (not broken test) in allure report
    """
    ...


def validate(data: dict, schema: Schema, attach_schema_to_report: Optional[bool] = True) -> None:
    """
    Function for dict validation

    :param data: Dict to validate
    :param schema: Schema object
    :param attach_schema_to_report: Attach json schema to allure report or not

    :return: None
    """
    LOGGER.info('Trying to validate dict with schema "%s"' % schema.name)
    if attach_schema_to_report:
        attach_dict_to_report(schema.json_schema(1), name='Validation schema')
    try:
        schema.validate(data)
    except SchemaError as exception:
        LOGGER.warning('Validation failed')
        raise JsonSchemaValidationError('Dict failed validation') from exception
    LOGGER.info('Validation succeeded')
