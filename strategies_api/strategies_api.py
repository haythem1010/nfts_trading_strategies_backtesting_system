from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from strategies.bollinger_band.signals import Backtesting

backtest = Backtesting()
app = Flask(__name__)
api = Api(app)

class BollingerAPI(Resource):
    def get(self, window, collection, days):
        trades, trading_data = backtest.backtest_bollinger_band(collection, window, days)

        return trades, trading_data


api.add_resource(BollingerAPI, '/indexes/gaming/<int:days>/<int:window>/<str:collection>')

# class BuyTheFloorAPI(Resource):
