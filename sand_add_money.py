from tinkoff.invest import Client, MoneyValue
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from environs import Env

env = Env()
env.read_env()

TOKEN = env('TOKEN_SAND')

with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
    # sb = client.sandbox
    id_ac = client.users.get_accounts().accounts[0].id
    client.sandbox.sandbox_pay_in(
        account_id=id_ac,
        amount=MoneyValue(units=1000, nano=0, currency='rub')
    )
    r = client.operations.get_portfolio(account_id=id_ac)
    print(r)
