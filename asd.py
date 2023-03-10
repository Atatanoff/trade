from datetime import datetime, timedelta

from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle

import creds
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def run():

    try:
        with Client(creds.token_ro_acc_main) as client:
            r = client.market_data.get_candles(
                figi='BBG004S68BR5',
                from_=datetime.utcnow() - timedelta(days=1),
                to=datetime.utcnow(),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN # см. utils.get_all_candles
            )

            df = create_df(r.candles)
            
            df['ema'] = ema_indicator(close=df['close'], window=9)

            df.to_csv('share_data.txt', header=True, sep='\t', mode='w')
            print(df[['time', 'close', 'ema']].tail(30))
            ax=df.plot(x='time', y='close')
            df.plot(ax=ax, x='time', y='ema')
            plt.show()

    except RequestError as e:
        print(str(e))


def create_df(candles):
    df = DataFrame([{
        'time': candle.time,
        'volume': candle.volume,
        'open': cast_money(candle.open),
        'close': cast_money(candle.close),
        'high': cast_money(candle.high),
        'low': cast_money(candle.low),
    } for candle in candles])
    
    return df


def cast_money(v):

    return v.units + v.nano / 1e9 # nano - 9 нулей


