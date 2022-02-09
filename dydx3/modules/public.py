import aiohttp

from dydx3.helpers.request_helpers import generate_query_path
from dydx3.helpers.requests import request


class Public(object):

    def __init__(
        self,
        host,
        session: aiohttp.ClientSession,
    ):
        self.host = host
        self.session = session

    # ============ Request Helpers ============

    async def _get(self, request_path, params={}):
        return await request(self.session,
            generate_query_path(self.host + request_path, params),
            'get',
        )

    async def _put(self, endpoint, data):
        return await request(self.session,
            self.host + '/v3/' + endpoint,
            'put',
            {},
            data,
        )

    # ============ Requests ============

    async def check_if_user_exists(self, ethereum_address):
        '''
        Check if user exists

        :param host: required
        :type host: str

        :returns: Bool

        :raises: DydxAPIError
        '''
        uri = '/v3/users/exists'
        return await self._get(
            uri,
            {'ethereumAddress': ethereum_address},
        )

    async def check_if_username_exists(self, username):
        '''
        Check if username exists

        :param username: required
        :type username: str

        :returns: Bool

        :raises: DydxAPIError
        '''
        uri = '/v3/usernames'
        return await self._get(uri, {'username': username})

    async def get_markets(self, market=None):
        '''
        Get one or more markets

        :param market: optional
        :type market: str in list [
            "BTC-USD",
            "ETH-USD",
            "LINK-USD",
            ...
        ]

        :returns: Market array

        :raises: DydxAPIError
        '''
        uri = '/v3/markets'
        return await self._get(uri, {'market': market})

    async def get_orderbook(self, market):
        '''
        Get orderbook for a market

        :param market: required
        :type market: str in list [
            "BTC-USD",
            "ETH-USD",
            "LINK-USD",
            ...
        ]

        :returns: Object containing bid array and ask array of open orders
        for a market

        :raises: DydxAPIError
        '''
        uri = '/'.join(['/v3/orderbook', market])
        return await self._get(uri)

    async def get_stats(self, market=None, days=None):
        '''
        Get one or more day statistics for a market

        :param market: optional
        :type market: str in list [
            "BTC-USD",
            "ETH-USD",
            "LINK-USD",
            ...
        ]

        :param days: optional
        :type days: str in list [
            "1",
            "7",
            "30",
        ]

        :returns: Statistic information for a market, either for all time
        periods or just one.

        :raises: DydxAPIError
        '''
        uri = (
            '/'.join(['/v3/stats', market])
            if market is not None
            else '/v3/stats'
        )

        return await self._get(uri, {'days': days})

    async def get_trades(self, market, starting_before_or_at=None):
        '''
        Get trades for a market

        :param market: required
        :type market: str in list [
            "BTC-USD",
            "ETH-USD",
            "LINK-USD",
            ...
        ]

        :param starting_before_or_at: optional
        :type starting_before_or_at: str

        :returns: Trade array

        :raises: DydxAPIError
        '''
        uri = '/'.join(['/v3/trades', market])
        return await self._get(
            uri,
            {'startingBeforeOrAt': starting_before_or_at},
        )

    async def get_historical_funding(self, market, effective_before_or_at=None):
        '''
        Get historical funding for a market

        :param market: required
        :type market: str in list [
            "BTC-USD",
            "ETH-USD",
            "LINK-USD",
            ...
        ]

        :param effective_before_or_at: optional
        :type effective_before_or_at: str

        :returns: Array of historical funding for a specific market

        :raises: DydxAPIError
        '''
        uri = '/'.join(['/v3/historical-funding', market])
        return await self._get(
            uri,
            {'effectiveBeforeOrAt': effective_before_or_at},
        )

    async def get_fast_withdrawal(
        self,
        creditAsset=None,
        creditAmount=None,
        debitAmount=None,
    ):
        '''
        Get all fast withdrawal account information

        :param creditAsset: optional
        :type creditAsset: str

        :param creditAmount: optional
        :type creditAmount: str

        :param debitAmount: optional
        :type debitAmount: str

        :returns: All fast withdrawal accounts

        :raises: DydxAPIError
        '''
        uri = '/v3/fast-withdrawals'
        return await self._get(
            uri,
            {
                'creditAsset': creditAsset,
                'creditAmount': creditAmount,
                'debitAmount': debitAmount,
            },
        )

    async def get_candles(
        self,
        market,
        resolution=None,
        from_iso=None,
        to_iso=None,
        limit=None,
    ):
        '''
        Get Candles

        :param market: required
        :type market: str in list [
            "BTC-USD",
            "ETH-USD",
            "LINK-USD",
            ...
        ]

        :param resolution: optional
        :type resolution: str in list [
            "1DAY",
            "4HOURS"
            "1HOUR",
            "30MINS",
            "15MINS",
            "5MINS",
            "1MIN",
        ]

        :param from_iso: optional
        :type from_iso: str

        :param to_iso: optional
        :type to_iso: str

        :param limit: optional
        :type limit: str

        :returns: Array of candles

        :raises: DydxAPIError
        '''
        uri = '/'.join(['/v3/candles', market])
        return await self._get(
            uri,
            {
                'resolution': resolution,
                'fromISO': from_iso,
                'toISO': to_iso,
                'limit': limit,
            },
        )

    async def get_time(self):
        '''
        Get api server time as iso and as epoch in seconds with MS

        :returns: ISO string and Epoch number in seconds with MS of server time

        :raises: DydxAPIError
        '''
        uri = '/v3/time'
        return await self._get(uri)

    async def verify_email(
        self,
        token,
    ):
        '''
        Verify email with token

        :param token: required
        :type token: string

        :returns: empty object

        :raises: DydxAPIError
        '''
        return await self._put(
            'emails/verify-email',
            {
                'token': token,
            }
        )

    async def get_public_retroactive_mining_rewards(
        self,
        ethereum_address,
    ):
        '''
        Get public retroactive mining rewards

        :param ethereumAddress: required
        :type ethereumAddress: str

        :returns: PublicRetroactiveMiningRewards

        :raises: DydxAPIError
        '''
        return await self._get(
            '/v3/rewards/public-retroactive-mining',
            {
                'ethereumAddress': ethereum_address,
            },
        )

    async def get_config(self):
        '''
        Get global config variables for the exchange as a whole.
        This includes (but is not limited to) details on the exchange,
        including addresses, fees, transfers, and rate limits.

        :returns: GlobalConfigVariables

        :raises: DydxAPIError
        '''
        return await self._get('/v3/config')
