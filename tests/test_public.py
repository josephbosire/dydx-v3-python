import os

import pytest

from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, API_HOST_MAINNET
from dydx3.constants import MARKET_STATISTIC_DAY_ONE

from tests.constants import DEFAULT_HOST

ADDRESS_1 = '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C0'
API_HOST = os.environ.get('V3_API_HOST', API_HOST_MAINNET)

class TestPublic():


    @pytest.mark.asyncio
    async def test_check_if_user_exists(self):
        public = Client(API_HOST).public
        resp = await public.check_if_user_exists(ADDRESS_1)
        assert resp.data == {'exists': False}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_check_if_username_exists(self):
        public = Client(API_HOST).public
        resp = await public.check_if_username_exists('foo')
        assert resp.data == {'exists': False}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_markets(self):
        public = Client(API_HOST).public
        resp = await public.get_markets()
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_orderbook(self):
        public = Client(API_HOST).public
        resp = await public.get_orderbook(MARKET_BTC_USD)
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_stats(self):
        public = Client(API_HOST).public
        resp = await public.get_stats(
            MARKET_BTC_USD,
            MARKET_STATISTIC_DAY_ONE,
        )
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_trades(self):
        public = Client(API_HOST).public
        resp = await public.get_trades(MARKET_BTC_USD)
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_historical_funding(self):
        public = Client(API_HOST).public
        resp = await public.get_historical_funding(MARKET_BTC_USD)
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_candles(self):
        public = Client(API_HOST).public
        resp = await public.get_candles(MARKET_BTC_USD)
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_get_fast_withdrawal(self):
        public = Client(API_HOST).public
        resp = await public.get_fast_withdrawal()
        assert resp.data != {}
        assert resp.headers != {}

    @pytest.mark.asyncio
    async def test_verify_email(self):
        try:
            public = Client(API_HOST).public
            await public.verify_email('token')
        except Exception as e:
            # No userId gotten with token: token so no verification
            # has occurred
            assert e.status_code == 400

    @pytest.mark.asyncio
    async def test_public_retroactive_mining(self):
        public = Client(API_HOST).public
        resp = await public.get_public_retroactive_mining_rewards(ADDRESS_1)
        assert resp.data != {}
        assert resp.headers != {}
