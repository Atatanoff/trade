
from tinkoff.invest import Client, InstrumentIdType
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from environs import Env


env = Env()
env.read_env()


TOKEN = env("INVEST_R_TOKEN")
ID = env('ID')

def log(per):
    with open('log.txt', 'a') as file:
        print(per, '/n', file=file)

def create_df(candles : [HistoricCandle]):
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])

    return df

def cast_money(v):
    return v.units + v.nano / 1e9 # nano - 9 нулей


def main():
    figi = 'BBG000FXW512'
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        log(client.operations.get_portfolio(account_id=ID))

    



if __name__ == "__main__":
    main()