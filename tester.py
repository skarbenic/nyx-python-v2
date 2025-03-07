from get_usdt_class import GetUsdtBalance
import config as c
import asyncio
async def main():
    usdt_handler = GetUsdtBalance()
    usdt_balance = await usdt_handler.fetch_usdt_balance()
    print(usdt_balance)
    
asyncio.run(main())