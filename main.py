
from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBO
from environs import Env

env = Env()
env.read_env()

TOKEN = env('TOKEN_SAND')


def main():
    pass

if __name__=='__main__':
    main()
