import datetime
from pandas import DataFrame
from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from config.config import TOKEN
import pandas as pd
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX


class BotTrad:
    def __init__(self):
        self.bot_status = 'buy'

    def get_status_share(self):
        pass

    # def create_df(candles: [HistoricCandle]):
    #     df = DataFrame([{
    #         'time': c.time,
    #         'volume': c.volume,
    #         'open': cast_money(c.open),
    #         'close': cast_money(c.close),
    #         'high': cast_money(c.high),
    #         'low': cast_money(c.low),
    #     } for c in candles])
    #
    #     return df


def log(per, name: str = 'log.log', act: str = 'a'):
    t = datetime.datetime.now()
    with open(name, act) as file:
        print(t, ' ', per, '/n', file=file)


def cast_money(v):
    return v.units + v.nano / 1e9  # nano - 9 нулей


def get_figi(ticker: str):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as cl:
        instruments: InstrumentsService = cl.instruments

        list_shares = instruments.shares().instruments

        df = DataFrame(list_shares, columns=['name', 'figi', 'ticker', 'class_code'])

        df = df[df['ticker'] == ticker]
        if df.empty:
            print(f"Нет тикера {ticker}")
            return False

        return df['figi'].iloc[0]


if __name__ == '__main__':
    print(get_figi('NMTP'))
