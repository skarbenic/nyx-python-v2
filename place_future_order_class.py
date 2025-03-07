from init_binance_client import init_binance_client as ibc
from get_usdt_class import GetUsdtBalance
from telegram_handler_class import TelegramHandler
import config as c
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json_formatter
from binance.enums import *

executor = ThreadPoolExecutor(max_workers=2)

class PlaceFutureOrder:
    def __init__(self, trading_pair, side, usdt_balance):
        self.binance_client = ibc()
        self.trading_pair = trading_pair
        self.side = side.upper()
        self.usdt_balance = usdt_balance
        self.leverage = c.LEVERAGE 
        self.percentage = c.BUY_PERCENTAGE if self.side == 'BUY' else c.SHORT_PERCENTAGE
        self.precision = None
        self.precision_info = None
        
        
    async def get_precision(self):
        loop = asyncio.get_running_loop()       
        self.precision_info = await loop.run_in_executor(executor, self.binance_client.futures_exchange_info)
        if not self.precision_info or 'symbols' not in self.precision_info:
            raise ValueError('Failed to fetch exchange info')
        self.percent_price_filter = None
        for s in self.precision_info['symbols']:
            if s['symbol'] == self.trading_pair:
                self.precision = s['quantityPrecision']
                for f in s['filters']:
                    if f['filterType'] == 'PERCENT_PRICE':
                        self.percent_price_filter = f #Might be useful later
                return
        raise ValueError(f"Trading pair {self.trading_pair} is not found in exchange info")
        
        
    async def calculate_quantity(self):
        if self.precision is None:
            raise ValueError("Precision has not received any value yet, Call get_precision first")
        
        if not isinstance(self.usdt_balance, (int, float)):
            raise ValueError(f'usdt_balance must be a number, got {type(self.usdt_balance)}')
        
        #Use usdt_balance passed to __init__, no need to fetch
        amount_to_use = self.usdt_balance * self.percentage
        buying_power = amount_to_use * self.leverage
        
        #Async to get market price
        loop = asyncio.get_running_loop()
        ticker = await loop.run_in_executor(None, lambda: self.binance_client.futures_symbol_ticker)
        price = float(ticker['price']) #e.g SOLUSDT price = 150 USDT per sol
        quantity = buying_power / price
        return round(quantity, self.precision)    
    
    async def place_order(self, quantity):
        try:
            loop = asyncio.get_running_loop()
            # CHANGE THE LEVERAGE FIRST SO THE MATH IS MATHING
            await loop.run_in_executor(executor, lambda: self.binance_client.futures_change_leverage(
                symbol=self.trading_pair,
                leverage=self.leverage
            ))
            order = await loop.run_in_executor(executor,lambda: self.binance_client.futures_create_order(
                symbol=self.trading_pair,
                side=self.side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            ))
            print(f'Order placed: {order}')
            return order
        except Exception as e:
            print(f'Error placing order: {e}')
            return None
