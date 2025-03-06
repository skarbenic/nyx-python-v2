from telethon import TelegramClient, events
from json_formatter import log_to_json
from binance.client import Client
from init_binance_client import init_binance_client
import config as c
import re
import time

client = TelegramClient('jan', c.api_id, c.api_hash)

class TelegramHandler:
    def __init__(self, api_id=c.api_id, api_hash=c.api_hash, channel_id=c.channel_id):
        self.client = TelegramClient('jan', api_id, api_hash)
        self.channel_id = channel_id
        self.captured_symbol = None
        self.captured_action = None
        self.last_message_id = None
        self.last_order_time = 0
        self.COOLDOWN_PERIOD = c.COOLDOWN_PERIOD
        self.binance_client = init_binance_client()
        

    def setup_telegram_handler(self):
        @self.client.on(events.NewMessage(chats=self.channel_id))
        async def handle_new_message(event):
            from place_future_order_class import PlaceFutureOrder
            from get_usdt_class import GetUsdtBalance
            message = event.message.text
            current_time = time.time()
            match = re.match(r'#(\w+)\s+([\w/]+)', message)

            if message:
                if self.last_message_id is not None and event.message.id == self.last_message_id and (current_time - self.last_order_time < self.COOLDOWN_PERIOD):
                    log_to_json({'message': 'Duplicate detected within cooldown period, skipping message.'})
                    return
            if match:
                self.captured_symbol = match.group(1)
                self.captured_action = match.group(2)
                trading_pair = (self.captured_symbol + 'USDT').upper()
                if trading_pair.upper() in c.blacklist:
                    print(f'Symbol {valid_symbol} is blacklisted, ignoring the message. Check config.py for full blacklisted symbols.')
                    return
                
                try: 
                    exchange_info = self.binance_client.futures_exchange_info()
                    symbols = [s['symbol'] for s in exchange_info['symbols']]
                    valid_symbol = self.captured_symbol.upper() + 'USDT'
                    if valid_symbol in symbols:
                        log_to_json({
                            'symbol': (self.captured_symbol or '').upper(),
                            'action': (self.captured_action or '').upper(),
                            'timestamp': time.strftime('%d-%m-%Y, %H:%M:%S')
                        })
                        self.last_message_id = event.message.id # update the last message id so no duplicates
                        self.last_order_time = current_time
                        #Pass values from GetUsdtHandler
                        usdt_handler = GetUsdtBalance()
                        usdt_balance = await usdt_handler.fetch_usdt_balance()
                        #Pass values from PlaceFutureOrder
                        order = PlaceFutureOrder(trading_pair.upper(), self.captured_action, usdt_balance)
                        await order.get_precision() #THIS IS IMPORTANT TO MAKE SURE PRECISION HAS A VALUE!
                        quantity = order.calculate_quantity()
                        await order.place_order(quantity)
                        
                    else:
                        print(f'Error {self.captured_symbol} not found!')
                except Exception as e:
                    print(f'Error checking symbol: {e}')
        return self.client
    
    def trading_pair(self):
        return self.captured_symbol
    
    def side(self):
        return self.captured_action