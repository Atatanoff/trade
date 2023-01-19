
from project.project import get_figi, BotTrad, get_status_share

TICKER = "TMOS"


def run():
    figi = get_figi(TICKER)
    #bot = BotTrad(figi)
    get_status_share()
    # while True:
    #     try:
    #         get_status_share()
    #     except Exception: log(Exception)


if __name__ == '__main__':
    run()
