from pprint import pprint

from utils.helpers import percent_change


class BolingerBandRiskMngmnt(object):

    @staticmethod
    def take_profit_rule(trades, target_profit):
        i = 1
        while i < len(trades):
            if trades[i]['action'] == 'hold' and percent_change(trades[i-1]['price'],trades[i]['price']) > (target_profit / 100):
                trades[i]['indicator'] = 'sell for profit'
            else:
                trades[i]['indicator'] = "--"
            i = i+1

    @staticmethod
    def stop_loss_rule(trades, loss_permited):
        i = 1
        while i < len(trades):
            if trades[i]['action'] == 'hold' and percent_change(trades[i - 1]['price'],trades[i]['price']) < (-loss_permited / 100):
                trades[i]['indicator'] = 'sell to avoid loss'
            i = i + 1
