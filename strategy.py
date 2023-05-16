# strategy.py

import numpy as np
import pandas as pd
from sklearn.svm import SVR
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from importlib import import_module
from api import get_historical_data, place_order

def train_svr_model(df):
    x = df['close'].values
    y = df['close'].shift(-1).values
    svr = SVR()
    svr.fit(x, y)
    return svr

# strategy.py

def execute_strategy(symbol, amount):
    df = get_historical_data(symbol, '1day')
    if df is not None:
        ema = EMAIndicator(df['close'], window=200)
        rsi = RSIIndicator(df['close'], window=14)
        current_price = df['close'].iloc[-1]
        svr = train_svr_model(df)
        prediction = svr.predict(df['close'].values)

        # Initialize order to None
        order = None

        # Check if the EMA and RSI are in a buy signal
        if ema.ema_indicator() > current_price and rsi.rsi() < 30:
            order = {
                'symbol': symbol,
                'type': 'buy-market',
                'amount': amount
            }

        # Check if the EMA and RSI are in a sell signal
        elif ema.ema_indicator() < current_price and rsi.rsi() > 70:
            order = {
                'symbol': symbol,
                'type': 'sell-market',
                'amount': amount
            }

        # Place the order if there is one
        if order is not None:
            try:
                success = place_order(order)
                if success:
                    return "Trade executed successfully"
                else:
                    return "Failed to execute trade"
            except Exception as e:
                return str(e)
    else:
        return "Failed to get historical data"

        # Place the order
        try:
            place_order(order)
        except Exception as e:
            print(e)