
from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBO
from config.config import TOKEN
from project.project import get_status_share, log



def run():
    while True:
        try:
            get_status_share()
        except Exception: log(Exception)

if __name__=='__main__':
    run()

