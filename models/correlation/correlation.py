from pprint import pprint
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from repository.transactions_stats_repo import TransactionsStatsRepository
import pandas as pd


def data_correlation(data):
    df = pd.DataFrame(data)
    sns.set_theme(style='white')
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    cmap = sns.diverging_palette(140, 20, as_cmap=True)
    heat = sns.heatmap(corr, annot=True, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0, square=True, linewidths=3, cbar_kws={"shrink": .5}, annot_kws={"fontsize": 8})
    heat.set_xticklabels(heat.get_xticklabels(), rotation=30, ha='right', fontsize=8)
    heat.set_yticklabels(heat.get_yticklabels(), rotation=0, fontsize=8)
    plt.xlabel('X-axis', fontsize=1)

    plt.show()

    return 0


class Correlation(object):
    stats = TransactionsStatsRepository()


    def data_preparation(self, collection, timeframe):
        trading_data, listing_data = self.stats.class_launcher(collection, timeframe)
        data = []

        i = 0

        while i < len(listing_data) and i < len(trading_data) and trading_data[i]['date'] == listing_data[i]['date']:
            data.append({"date": listing_data[i]["date"],
                            "listed_elements": listing_data[i]["ls_count"],
                            "transaction_count": trading_data[i]["tr_count"],
                            "floor_price": listing_data[i]["ls_min_price"],
                            "minimum_trading_price": trading_data[i]["tr_min_price"],
                            "maximum_trading_price": trading_data[i]["tr_max_price"],
                            "average_trading_price": trading_data[i]["tr_avg_price"],
                            "minimum_listing_price": listing_data[i]["ls_min_price"],
                            "maximum_listing_price": listing_data[i]["ls_min_price"],
                            "average_listing_price": listing_data[i]["ls_avg_price"]})
            i = i + 1
        return data

    def class_launcher(self,collection, window):
        corr_data = self.data_preparation(collection, window)
        data_correlation(corr_data)

        return 0



cor = Correlation()
data = cor.class_launcher('C3', 60*12)