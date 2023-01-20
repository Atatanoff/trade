import os
from datetime import datetime


def write(args):
    
    col = 30
    message = f'|{args[0].center(col, " ")}|{args[1].center(col," ")}|{args[2].center(col," ")}|{args[3].center(col," ")}|'
    try:
        with open('log/buysell.txt', 'a') as file:
            print(message, file=file)
    except Exception as e: log(e)


def write_file(args):
    t = datetime.now()
    if not os.path.exists('log/buysell.txt'):
        cols = (
            " ",
            "Цена инструмента",
            "Сумма покупки/продажи",
            "Коммисия",
        )
        write(cols)
    write((str(t), args[0], args[1], args[2]))



if __name__=='__main__':
    write_file(('2.23', '2,23445', '0,123'))
    write_file(('2.23', '2,23445', '0,123'))