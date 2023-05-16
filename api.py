# api.py
import requests
import pandas as pd
import json
from config import api_key, api_secret

base_url = 'https://api.huobi.pro'
klines_url = f'{base_url}/market/history/kline'
order_url = f'{base_url}/v1/order/orders/place'

def get_historical_data(symbol, period):
    response = requests.get(klines_url, params={'symbol': symbol, 'period': period})
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'])
        return df
    else:
        return None

def place_order(order, symbol):
    # You will likely need to sign your request here, as per the Huobi API documentation.
    # This may require additional implementation beyond just including the API key and secret in the headers.
    headers = {
        'AccessKeyId': api_key,
        'Signature': api_secret,
        'Content-Type': 'application/json'
    }
    response = requests.post(order_url, data=json.dumps(order), headers=headers)
    return response.status_code == 200

def get_current_price(symbol):
    response = requests.get(f'{base_url}/market/detail?symbol={symbol.lower()}usdt')
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'price' in data:
            return float(data['price'])
    return None
