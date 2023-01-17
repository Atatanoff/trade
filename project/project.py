import datetime


class BotTrad:
    def __init__(self):
        self.bot_status = 'buy'


    def cast_money(v):
        return v.units + v.nano / 1e9  # nano - 9 нулей


    def get_status_share(self):
        pass


    def create_df(candles: [HistoricCandle]):
        df = DataFrame([{
            'time': c.time,
            'volume': c.volume,
            'open': cast_money(c.open),
            'close': cast_money(c.close),
            'high': cast_money(c.high),
            'low': cast_money(c.low),
        } for c in candles])

        return df


    def log(per, name: str = 'log.log', act: str = 'a'):
        t = datetime.datetime.now()
        with open(name, act) as file:
            print(t, ' ', per, '/n', file=file)
