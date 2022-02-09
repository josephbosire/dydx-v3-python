import json

import aiohttp as aiohttp

from dydx3.errors import DydxApiError
from dydx3.helpers.request_helpers import remove_nones

# TODO: Use a separate session per client instance.
core_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'dydx/python',
}


class Response(object):
    def __init__(self, data={}, headers=None):
        self.data = data
        self.headers = headers


async def request(session: aiohttp.ClientSession, uri, method, headers=None, data_values=None):
    if data_values is None:
        data_values = {}
    if headers is None:
        headers = {}
    response = await send_request(
        session,
        uri,
        method,
        headers,
        data=json.dumps(
            remove_nones(data_values)
        )
    )
    if not str(response.status).startswith('2'):
        raise DydxApiError.create(response)

    if response.content:
        return Response(await response.json(), response.headers)
    else:
        return Response('{}', response.headers)


async def send_request(session: aiohttp.ClientSession, uri, method, headers=None, **kwargs) -> aiohttp.ClientResponse:
    if headers is None:
        headers = {}
    return await getattr(session, method)(uri, headers={**core_headers, **headers}, **kwargs)
