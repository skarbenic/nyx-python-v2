from telethon import TelegramClient, events
from json_formatter import log_to_json
from binance.client import Client
from init_binance_client import init_binance_client
import config as c
import re
import time

client = TelegramClient('jan', c.api_id, c.api_hash)

class TelegramHandler:
    def __init__(self, api_id=c.api_id, api_hash=c.api_hash, channel_id=c.test_channel_id):
        self.client = TelegramClient('jan', api_id, api_hash)
        self.channel_id = channel_id
        self.captured_symbol = ''
        self.captured_action = ''
        self.last_message_id = ''
        self.last_order_time = 0
        self.COOLDOWN_PERIOD = 60
        self.binance_client = init_binance_client()

    def setup_telegram_handler(self):
        @self.client.on(events.NewMessage(chats=self.channel_id))
        async def handle_new_message(event):
            message = event.message.text
            current_time = time.time()
            match = re.match(r'#(\w+)\s+([\w/]+)', message)

            if message:
                if event.message.id == self.last_message_id and (current_time - self.last_order_time < self.COOLDOWN_PERIOD):
                    return
            if match:
                captured_symbol = match.group(1)
                captured_action = match.group(2)
                try: 
                    exchange_info = self.binance_client.futures_exchange_info()
                    symbols = [s['symbol'] for s in exchange_info['symbols']]
                    valid_symbol = captured_symbol + 'USDT'
                    if valid_symbol in symbols:
                        self.captured_symbol = captured_symbol
                        self.captured_action = captured_action
                        log_to_json({'symbol': self.captured_symbol, 'action': self.captured_action})
                        self.last_message_id = event.message.id # update the last message id so no duplicates
                        self.last_order_time = current_time
                    else:
                        print(f'{captured_symbol} not found.')
                except Exception as e:
                    print(f'Error checking symbol: {e}')
        return self.client
    
    def trading_pair(self):
        return self.captured_symbol
    
    def side(self):
        return self.captured_action