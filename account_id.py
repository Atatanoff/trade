from tinkoff.invest import Client
from config.config import TOKEN
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX, INVEST_GRPC_API






with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
    print(client.users.get_accounts())
    
