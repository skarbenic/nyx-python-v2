import asyncio
from telegram_handler import client, setup_telegram_handler
import config as c

async def main():
    client = setup_telegram_handler()
    print('Starting client')
    await client.start(phone=c.phone)
    print(f'Connected to client, {c.phone}. Listening for messages.')
    while True:
        try:
            await client.run_until_disconnected()
        except Exception as e:
            print(f'Error: {e}, reconnecting in 5s')
            await asyncio.sleep(5)
            await client.connect()
    
if __name__ == '__main__':
    asyncio.run(main())
            