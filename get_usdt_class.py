from init_binance_client import init_binance_client
import config as c
import asyncio

class GetUsdtBalance:
    def __init__(self, api_key=c.binance_api, api_secret=c.binance_secret):
        self.binance_client = init_binance_client()
        self.usdt_balance = None #initialize balance as None first here

    async def fetch_usdt_balance(self):
        loop = asyncio.get_running_loop()
        balances = await loop.run_in_executor(None, self.binance_client.futures_account_balance)
        if not balances:
            raise ValueError(f"Failed to fetch balances: {balances}")
        
        for asset in balances:
            if asset['asset'] == 'USDT':
                self.usdt_balance = float(asset['balance'])
                return self.usdt_balance
        raise ValueError('USDT Balance not found in response')
    
    def get_usdt(self):
        if self.usdt_balance is not None:
            return self.usdt_balance
        else:
            raise ValueError("USDT balance not available yet.")