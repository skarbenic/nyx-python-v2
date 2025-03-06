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
        
        
    def calculate_quantity(self):
        if self.precision is None:
            raise ValueError("Precision has not received any value yet!")
        amount_to_use = (self.usdt_balance * self.percentage)
        quantity = (amount_to_use * self.leverage)
        return round(quantity, self.precision)
    
    async def place_order(self):
        try:
            loop = asyncio.get_running_loop()
            order = await loop.run_in_executor(executor,lambda: self.binance_client.futures_create_order(
                symbol=self.trading_pair,
                side=self.side,
                type=ORDER_TYPE_MARKET,
                quantity=self.calculate_quantity()
            ))
            print(f'Order placed: {order}')
            return order
        except Exception as e:
            print(f'Error placing order: {e}')
            return None
