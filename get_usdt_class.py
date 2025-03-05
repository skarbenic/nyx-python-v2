from init_binance_client import init_binance_client
import config as c
import asyncio

class GetUsdtBalance:
    def __init__(self, api_key, api_secret):
        self.binance_client = init_binance_client()
        self.usdt_balance = None

    async def fetch_usdt_balance(self):
        loop = asyncio.get_running_loop()
        account_info = await loop.run_in_executor(None, self.binance_client.futures_account)
        if not account_info:
            raise ValueError(f"Failed to fetch account info: {account_info}")
        self.usdt_balance = float(account_info['totalWalletBalance'])
        return self.usdt_balance
    
    def get_usdt(self):
        if self.usdt_balance is not None:
            return self.usdt_balance
        else:
            raise ValueError("USDT balance not available yet.")