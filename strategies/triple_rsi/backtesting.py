class Backtesting(object):
    @staticmethod
    def trades(data):
        trades = []
        for i in data:
            if i['action'] != '--':
                trades.append({'date': i['date'], 'action': i['action'], 'price': i['average_trading_price']})

        profit = 0
        for i in trades:
            if i['action'] == 'buy':
                profit = profit - i['price']
            elif i['action'] == 'sell':
                profit = profit + i['price']

        return trades, profit