import ccxt
import time
import numpy as np


bitmex = ccxt.bitmex()
symbol = 'ETH/USD'
symbol_last_price = bitmex.fetch_ticker(symbol)['last']

interval = 60 * 60
price_threshold = 0.01

eth_prices = []
btc_prices = []

while True:
    eth_current_price = bitmex.fetch_ticker(symbol)['last']

    eth_prices.append(eth_current_price)
    print(eth_prices)

    if len(eth_prices) >= interval:
        btc_current_price = bitmex.fetch_ticker('BTC/USD')['last']
        btc_prices.append(btc_current_price)
        correlation = np.corrcoef(eth_prices, btc_prices)[0, 1]

        if abs(correlation) < 0.1:
            mean_price = np.mean(eth_prices)
            price_change = (eth_current_price - mean_price) / mean_price

            if abs(price_change) >= price_threshold:
                print('Цена ETH изменилась на {:.2%} за последние 60 минут'.format(price_change))

        eth_prices = []
        btc_prices = []

    time.sleep(10)
