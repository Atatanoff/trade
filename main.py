
from project.project import log
from project.project import get_figi, BotTrad
from time import sleep
from project.format import write_file


TICKER = "TMOS"
INSTR = 'etfs'


def run():
    print('Погнали\n\n')
    figi = get_figi(TICKER, INSTR)
    print(f'Получили фиги): {figi}\n\n')
    bot = BotTrad(figi)
    print('Бот создан \n\n')
    print('(^.^)/  Hi!')
    # get_status_share()
    while True:
        sleep(1)
        try:
            bot.run()
        except Exception as e:
            print(e)
            log(e)


if __name__ == '__main__':
    run()
    
