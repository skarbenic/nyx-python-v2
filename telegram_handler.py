from telethon import TelegramClient, events
from json_formatter import log_to_json
import config as c
import re
import time

client = TelegramClient('jan', c.api_id, c.api_hash)

def setup_telegram_handler():
    @client.on(events.NewMessage(chats=c.channel_id))
    async def handle_new_message(event):
        global captured_symbol, captured_action, last_message, last_order_time, last_message_id
        message = event.message.text
        current_time = time.time()
        match = re.match(r'#(\w+)\s+([\w/]+)', message)
        
        if message:
            #Check for duplicate message to avoid firing double orders
            if event.message.id == c.last_message_id and (current_time - last_order_time < c.COOLDOWN_PERIOD):
                return
        if match:
            captured_symbol = match.group(1)
            captured_action = match.group(2)
            #Transform the message into stripping whitespace and uppercase
            normalized_message = message.strip().upper()
            
            log_to_json({'captured_symbol': captured_symbol, 'action': captured_action})
            c.last_message_id = event.message.id
    return client