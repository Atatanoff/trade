from datetime import datetime, timedelta

from tinkoff.invest import Client, RequestError, CandleInterval, OrderDirection, OrderType
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.constants import INVEST_GRPC_API

from config.config import TOKEN, ACCOUNT_ID, LOT_QUANT
from project.format import write_file

from ta.trend import ema_indicator

from pandas import DataFrame
import pandas as pd

import matplotlib.pyplot as plt


class BotTrad:
    def __init__(self, figi):
        
        self.figi = figi
        self.instr_buy = 0
        self.target = INVEST_GRPC_API
        self.price = 0
        self.get_status_instr()
        self.direction = OrderDirection.ORDER_DIRECTION_BUY if self.df['ema'].tail(1).iloc[0] < self.df['sma'].tail(1).iloc[0] else OrderDirection.ORDER_DIRECTION_SELL

    

    def buysell(self):
        try:
            with Client(TOKEN, target=self.target) as cl:
                r = cl.orders.post_order(
                    order_id=str(datetime.utcnow().timestamp()),
                    figi=self.figi,
                    quantity=LOT_QUANT,
                    account_id=ACCOUNT_ID,
                    direction=self.direction,
                    order_type=OrderType.ORDER_TYPE_MARKET
                )
                ex_pr = '-' if self.direction == OrderDirection.ORDER_DIRECTION_BUY else "" + str(r.executed_order_price)
                tot_or = '-' if self.direction == OrderDirection.ORDER_DIRECTION_BUY else "" + str(r.total_order_amount)
                ex_com = '-' + str(r.executed_commission)
                write_file((ex_pr, tot_or, ex_com))
                
                self.price = self.cast_money(r.executed_order_price)
        except Exception as e:
            self.log('Ошибка в фунции buysell: ', e)
            print('Ошибка в фунции buysell: ', e)
    
    
    def run(self):
        self.get_status_instr()

        if self.let_buy():
            # производим закупку
            self.buysell()      
            self.direction = OrderDirection.ORDER_DIRECTION_SELL
            self.instr_buy = self.df['close'].tail(1).iloc[0] * 0,98
            print(f'Купили фигу по цене {self.price}')

        elif self.let_sell() or self.df['close'].tail(1).iloc[0] < self.instr_buy:
            # производим продажу опциона
            self.buysell()
            self.direction = OrderDirection.ORDER_DIRECTION_BUY
            print(f'Продали фигу по цене {self.price}')


    def get_status_instr(self):
        try:
            with Client(TOKEN, target=self.target) as client:
                status_instr = client.market_data.get_candles(
                    figi=self.figi,
                    from_=datetime.utcnow() - timedelta(days=1),
                    to=datetime.utcnow(),
                    interval=CandleInterval.CANDLE_INTERVAL_1_MIN # см. utils.get_all_candles
                )
                
                self.create_df_candels(status_instr.candles)            
                self.df['ema'] = ema_indicator(close=self.df['close'], window=7)
                self.df['sma'] = ema_indicator(close=self.df['close'], window=14)
                self.df['ssma'] = ema_indicator(close=self.df['close'], window=21)
                print(f"{self.df['ema'].tail(1).iloc[0]} <===> {self.df['sma'].tail(1).iloc[0]}")
                
                                      

        except RequestError as e:
            self.log(str(e))
            print(str(e))


    def let_buy(self):
        return self.direction == OrderDirection.ORDER_DIRECTION_BUY and self.df['ema'].tail(1).iloc[0] >= self.df['sma'].tail(1).iloc[0]#\
                    #and self.df['ema'].tail(1).iloc[0] < self.df['sma'].tail(1).iloc[0] \
                    #and self.df['ema'].tail(1).iloc[0] < self.df['ssma'].tail(1).iloc[0]
    
    def let_sell(self):
        return self.direction == OrderDirection.ORDER_DIRECTION_SELL and self.df['ema'].tail(1).iloc[0] <= self.df['sma'].tail(1).iloc[0]


    def create_df_candels(self, candles):
        self.df = DataFrame([{
            'time': candle.time,
            'volume': candle.volume,
            'open': self.cast_money(candle.open),
            'close': self.cast_money(candle.close),
            'high': self.cast_money(candle.high),
            'low': self.cast_money(candle.low),
        } for candle in candles])       


    def cast_money(self, v):
        return v.units + v.nano / 1e9  # nano - 9 нулей

    
    @staticmethod
    def log(per, name: str = 'log.log', act: str = 'a'):
        t = datetime.now()
        
        with open(name, act) as file:
            print(t, ' ', per, '/n', file=file)


def get_status_share(figi = 'BBG004S68BR5'):
    try:
        with Client(TOKEN, target=INVEST_GRPC_API) as client:
            status_share = client.market_data.get_candles(
                figi=figi,
                from_=datetime.utcnow() - timedelta(days=1),
                to=datetime.utcnow(),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN # см. utils.get_all_candles
            )
            print(cast_money(status_share.candles[-1].close))
            df = create_df_candels(status_share.candles)
                        
            df['ema'] = ema_indicator(close=df['close'], window=2)
            df['sma'] = ema_indicator(close=df['close'], window=4)
            df['ssma'] = ema_indicator(close=df['close'], window=8)
            # df.to_csv('share_data.txt', header=True, sep='\t', mode='w')
            #print(df[['time', 'close', 'ema', 'sma']].tail(30))
            ax=df.plot(x='time', y='close')
            df.plot(ax=ax, x='time', y='ema')
            df.plot(ax=ax, x='time', y='sma')
            df.plot(ax=ax, x='time', y='ssma')
            plt.show()
            

    except RequestError as e:
        log(str(e))
        print(str(e))


def create_df_candels(candles):
    df = DataFrame([{
        'time': candle.time,
        'volume': candle.volume,
        'open': cast_money(candle.open),
        'close': cast_money(candle.close),
        'high': cast_money(candle.high),
        'low': cast_money(candle.low),
    } for candle in candles])
    
    return df



def log(per, name: str = 'log.log', act: str = 'a'):
    t = datetime.now()
    
    with open('log/'+name, act) as file:
        print(t, ' ', per, '/n', file=file)


def cast_money(v):
    return v.units + v.nano / 1e9  # nano - 9 нулей


def get_figi(ticker: str, instr: str):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    
    
    with Client(TOKEN, target=INVEST_GRPC_API) as cl:
        instruments: InstrumentsService = cl.instruments
        option = {
        'shares': instruments.shares().instruments,
        'etfs': instruments.etfs().instruments,
        'bonds': instruments.bonds().instruments,
        'currencies': instruments.currencies().instruments, # валюта
        'futures': instruments.futures().instruments,
        'options': instruments.options().instruments
        }
        list_shares = option[instr.lower()]
        df = DataFrame(list_shares, columns=['name', 'figi', 'ticker', 'class_code'])
        df = df[df['ticker'] == ticker]
        
        if df.empty:
            print(f"Нет тикера {ticker}")
            return False
        df.to_csv('share.txt', header=True, sep='\t', mode='w')
        
        return df['figi'].iloc[0]


if __name__ == '__main__':
    print(get_figi('NMTP'))
