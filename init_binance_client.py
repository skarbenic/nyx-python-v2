from binance.client import Client
import config as c
import time
import requests

def get_binance_server_time():
    response = requests.get('https://testnet.binancefuture.com/fapi/v1/time')
    server_time = response.json().get('serverTime')
    return server_time

def init_binance_client(api_key=c.channel_id, api_secret=c.binance_secret):
    server_time = get_binance_server_time()
    system_time = int(time.time() * 1000)
    time_offset = server_time - system_time #calculate time diff between binance server and local 
    
    binance_client = Client(c.binance_api, c.binance_secret, testnet=True)
    binance_client.API_URL = 'https://testnet.binancefuture.com/'
    binance_client.timestamp_offset = time_offset #adjust timestamp error
    return binance_client