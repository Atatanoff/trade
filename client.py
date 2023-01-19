
from tinkoff.invest import Client, InstrumentIdType
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from config.config import TOKEN


# def create_df(candles : [HistoricCandle]):
#     df = DataFrame([{
#         'time': c.time,
#         'volume': c.volume,
#         'open': cast_money(c.open),
#         'close': cast_money(c.close),
#         'high': cast_money(c.high),
#         'low': cast_money(c.low),
#     } for c in candles])

#     return df





def main():
    figi = 'BBG000FXW512'
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        log(client.operations.get_portfolio(account_id=ID))

    



if __name__ == "__main__":
    main()