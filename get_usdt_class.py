from init_binance_client import init_binance_client
import config as c
import asyncio

class GetUsdtBalance:
    def __init__(self, api_key=c.binance_api, api_secret=c.binance_secret):
        self.binance_client = init_binance_client()
        self.usdt_balance = None #initialize balance as None first here just to be sure and safe idk what im doing

    async def fetch_usdt_balance(self):
        loop = asyncio.get_running_loop()
        account_info = await loop.run_in_executor(None, self.binance_client.futures_account)
        if not account_info:
            raise ValueError(f"Failed to fetch account info: {account_info}")
        
        usdt_balance = float(account_info['totalWalletBalance'])
        return usdt_balance