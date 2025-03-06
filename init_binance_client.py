from binance.client import Client
import config as c

def init_binance_client(api_key=c.channel_id, api_secret=c.binance_secret):
    binance_client = Client(c.binance_api, c.binance_secret, testnet=True)
    binance_client.API_URL = 'https://testnet.binancefuture.com/'
    return binance_client