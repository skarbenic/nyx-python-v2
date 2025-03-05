from binance.client import Client
import config as c

def init_binance_client(api_key=c.test_channel_id, api_secret=c.testnet_binance_secret):
    binance_client = Client(c.testnet_binance_api, c.testnet_binance_secret, testnet=True)
    binance_client.API_URL = 'https://testnet.binancefuture.com/'
    return binance_client