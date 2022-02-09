import typing

import aiohttp


class DydxError(Exception):
    """Base error class for all exceptions raised in this library.
    Will never be raised naked; more specific subclasses of this exception will
    be raised when appropriate."""


class DydxApiError(DydxError):

    def __init__(self):
        self.status_code: typing.Optional[int] = None
        self.msg = None
        self.response: aiohttp.ClientResponse = None
        self.request: aiohttp.ClientRequest = None

    @staticmethod
    async def create(response: aiohttp.ClientResponse) -> 'DydxApiError':
        error = DydxApiError()
        error.status_code = response.status
        try:
            error.msg = await response.json()
        except ValueError:
            error.msg = await response.text()
        error.response = response
        error.request = getattr(response, 'request', None)

        return error

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'DydxApiError(status_code={}, response={})'.format(
            self.status_code,
            self.msg,
        )


class TransactionReverted(DydxError):

    def __init__(self, tx_receipt):
        self.tx_receipt = tx_receipt
