from environs import Env

env = Env()
env.read_env()

TOKEN = env('TOKEN_BUY')
ACCOUNT_ID = env('ACCOUNT_ID')
LOT_QUANT=1

