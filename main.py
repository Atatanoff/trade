from tinkoff.invest import Client
from config.config import TOKEN
from project.project import get_figi

TICKER = "NMTP"


def run():
    figi = get_figi(TICKER)

    # while True:
    #     try:
    #         get_status_share()
    #     except Exception: log(Exception)


if __name__ == '__main__':
    run()
