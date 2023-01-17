from pandas import DataFrame
from tinkoff.invest import Client, InstrumentStatus, SharesResponse, InstrumentIdType
from tinkoff.invest.services import InstrumentsService, MarketDataService
from config.config import TOKEN
import pandas as pd
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX

TICKER = "NMTP"

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def run():
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as cl:
        instruments: InstrumentsService = cl.instruments

        list_shares = instruments.shares().instruments

        df = DataFrame(list_shares, columns=['name', 'figi', 'ticker', 'class_code'])

        df = df[df['ticker'] == TICKER]
        if df.empty:
            print(f"Нет тикера {TICKER}")
            return

        print(df['figi'].iloc[0])


if __name__ == '__main__':
    run()
