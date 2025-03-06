import asyncio
from telegram_handler import client, setup_telegram_handler
from telegram_handler_class import TelegramHandler
import config as c

async def main():
    telegram_bot = TelegramHandler()
    client = telegram_bot.setup_telegram_handler()
    
    print('Starting the client')
    await client.start(phone=c.phone)
    print(f'Connected to client {c.phone}. Listening for messages....')
    
    try:
        await client.run_until_disconnected()
    except Exception as e:
        print(f'Error: {e}. Reconnecting in 5s.')
        await asyncio.sleep(5)
        await main()
        
if __name__ == "__main__":
    asyncio.run(main())