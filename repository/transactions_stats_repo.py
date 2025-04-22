from repository.sql_utils import SQLUtils
from utils.helpers import sql_to_dict
from time import time
from utils.helpers import convert_timestamp_to_date
sql = SQLUtils()


class TransactionsStatsRepository(object):

    @staticmethod
    def get_listing_stats_by_collection(collection, interval, ssh=sql.set_ssh_by_ip()):
        start = time()
        # print(sql.set_ssh_by_ip())
        query = f""" SELECT round(extract (epoch from DATE_TRUNC('minute',ls_stat.DATE))) * 1000 ::integer AS DATE,
                        ls_stat.ls_count::FLOAT,
                        ls_stat.ls_count  - LAG(ls_stat.ls_count) OVER (ORDER  BY ls_stat.date  )::FLOAT AS ls_count_change,
                        ROUND((ls_stat.ls_count  - LAG(ls_stat.ls_count) OVER (ORDER  BY ls_stat.date))/nullif(LAG(ls_stat.ls_count) OVER (ORDER  BY ls_stat.date),0)::NUMERIC,4)::FLOAT  AS ls_count_change_pct,
                        ls_stat.ls_min_price::FLOAT,
                        ls_stat.ls_min_price  - LAG(ls_stat.ls_min_price) OVER (ORDER  BY ls_stat.date  )::FLOAT AS ls_min_price_change,
                        ROUND((ls_stat.ls_min_price  - LAG(ls_stat.ls_min_price) OVER (ORDER  BY ls_stat.date))/nullif(LAG(ls_stat.ls_min_price) OVER (ORDER  BY ls_stat.date),0)::NUMERIC,4)::FLOAT AS ls_min_price_change_pct,
                        ls_stat.ls_max_price::FLOAT,
                        ls_stat.ls_max_price  - LAG(ls_stat.ls_max_price) OVER (ORDER  BY ls_stat.date  )::FLOAT AS ls_max_price_change,
                        ROUND((ls_stat.ls_max_price  - LAG(ls_stat.ls_max_price) OVER (ORDER  BY ls_stat.date))/nullif(LAG(ls_stat.ls_max_price) OVER (ORDER  BY ls_stat.date),0)::NUMERIC,4)::FLOAT AS ls_max_price_change_pct,
                        ls_stat.ls_avg_price::FLOAT,
                        ls_stat.ls_avg_price  - LAG(ls_stat.ls_avg_price) OVER (ORDER  BY ls_stat.date  )::FLOAT AS ls_avg_price_change,
                        ROUND((ls_stat.ls_avg_price  - LAG(ls_stat.ls_avg_price) OVER (ORDER  BY ls_stat.date))/nullif(LAG(ls_stat.ls_avg_price) OVER (ORDER  BY ls_stat.date),0)::NUMERIC,4)::FLOAT AS ls_avg_price_change_pct
                        FROM (SELECT (to_timestamp(floor((extract('epoch' from transaction_stat.date) / 
                        {interval * 60} )) * {interval * 60}) AT TIME ZONE 'UTC') as DATE, 
                        SUM(transaction_stat.ls_count) AS ls_count,
                        ROUND(MIN(transaction_stat.ls_min_price)::NUMERIC,4) AS ls_min_price,
                        ROUND(MAX(transaction_stat.ls_max_price)::NUMERIC,4) AS ls_max_price,
                        ROUND(AVG(transaction_stat.ls_avg_price)::NUMERIC,4) AS ls_avg_price
                        FROM transaction_stat WHERE transaction_stat.collection = '{collection}' GROUP BY 1 ORDER BY 1) ls_stat; """

        labels = ['date', 'ls_count', 'ls_count_change', 'ls_count_change_pct', 'ls_min_price', 'ls_min_price_change',
                  'ls_min_price_change_pct', 'ls_max_price', 'ls_max_price_change', 'ls_max_price_change_pct',
                  'ls_avg_price', 'ls_avg_price_change', 'ls_avg_price_change_pct']

        try:
            data = sql.execute_query(query=query, ssh=ssh)
            data = sql_to_dict(sql_data=data, labels=labels, type=2)
        except Exception as e:
            print(e)
            data = []

        for i in data:
            i['date'] = int(i['date'])
            i["date"] = convert_timestamp_to_date(i["date"], output_format='%Y-%m-%d %H:%M:%S')

        end = time()
        ex = end - start
        print("---------------------- listing data importers took  :", round(ex,3)," seconds ---------- ")
        return data


    @staticmethod
    def get_trading_stats_by_collection(collection, interval, ssh=sql.set_ssh_by_ip()):
        start = time()
        query = f"""SELECT round(extract (epoch from DATE_TRUNC('minute',tr_stat.DATE))) * 1000 AS DATE,
                        tr_stat.tr_count::FLOAT,
                        tr_stat.tr_count  - LAG(tr_stat.tr_count) OVER (ORDER  BY tr_stat.date  )::FLOAT AS tr_count_change,
                        ROUND((tr_stat.tr_count  - LAG(tr_stat.tr_count) OVER (ORDER  BY tr_stat.date))/nullif(LAG(tr_stat.tr_count) OVER (ORDER  BY tr_stat.date),0)::NUMERIC,4)::FLOAT  AS tr_count_change_pct,
                        tr_stat.tr_volume::FLOAT,
                        tr_stat.tr_volume  - LAG(tr_stat.tr_volume) OVER (ORDER  BY tr_stat.date  )::FLOAT AS tr_volume_change,
                        ROUND((tr_stat.tr_volume  - LAG(tr_stat.tr_volume) OVER (ORDER  BY tr_stat.date))/nullif(LAG(tr_stat.tr_volume) OVER (ORDER  BY tr_stat.date),0)::NUMERIC,4)::FLOAT AS tr_volume_change_pct,
                        tr_stat.tr_min_price::FLOAT,
                        tr_stat.tr_min_price  - LAG(tr_stat.tr_min_price) OVER (ORDER  BY tr_stat.date  )::FLOAT AS tr_min_price_change,
                        ROUND((tr_stat.tr_min_price  - LAG(tr_stat.tr_min_price) OVER (ORDER  BY tr_stat.date))/nullif(LAG(tr_stat.tr_min_price) OVER (ORDER  BY tr_stat.date),0)::NUMERIC,4)::FLOAT AS tr_min_price_change_pct,
                        tr_stat.tr_max_price::FLOAT,
                        tr_stat.tr_max_price  - LAG(tr_stat.tr_max_price) OVER (ORDER  BY tr_stat.date  )::FLOAT AS tr_max_price_change,
                        ROUND((tr_stat.tr_max_price  - LAG(tr_stat.tr_max_price) OVER (ORDER  BY tr_stat.date))/nullif(LAG(tr_stat.tr_max_price) OVER (ORDER  BY tr_stat.date),0)::NUMERIC,4)::FLOAT AS tr_max_price_change_pct,
                        tr_stat.tr_avg_price::FLOAT,
                        tr_stat.tr_avg_price  - LAG(tr_stat.tr_avg_price) OVER (ORDER  BY tr_stat.date  )::FLOAT AS tr_avg_price_change,
                        ROUND((tr_stat.tr_avg_price  - LAG(tr_stat.tr_avg_price) OVER (ORDER  BY tr_stat.date))/nullif(LAG(tr_stat.tr_avg_price) OVER (ORDER  BY tr_stat.date),0)::NUMERIC,4)::FLOAT AS tr_avg_price_change_pct
                        FROM (
                        SELECT (to_timestamp(floor((extract('epoch' from transaction_stat.date) / 
                        {interval * 60 } )) * {interval * 60}) AT TIME ZONE 'UTC') as DATE, 
                        SUM(transaction_stat.tr_count) AS tr_count,
                        ROUND(SUM(transaction_stat.tr_volume)::NUMERIC,4) AS tr_volume,
                        ROUND(MIN(transaction_stat.tr_min_price)::NUMERIC,4) AS tr_min_price,
                        ROUND(MAX(transaction_stat.tr_max_price)::NUMERIC,4) AS tr_max_price,
                        ROUND(AVG(transaction_stat.tr_avg_price)::NUMERIC,4) AS tr_avg_price
                        FROM transaction_stat WHERE transaction_stat.collection = '{collection}' GROUP BY 1 ORDER BY 1) tr_stat;"""
        labels = ['date','tr_count', 'tr_count_change','tr_count_change_pct','tr_volume','tr_volume_change','tr_volume_change_pct',
                  'tr_min_price','tr_min_price_change','tr_min_price_change_pct','tr_max_price',
                  'tr_max_price_change','tr_max_price_change_pct','tr_avg_price','tr_avg_price_change','tr_avg_price_change_pct']

        try:
            data = sql.execute_query(query=query, ssh=ssh)
            data = sql_to_dict(sql_data=data, labels=labels, type=2)
        except Exception as e:
            print(e)
            data = []

        for i in data:
            i['date'] = int(i['date'])
            i["date"] = convert_timestamp_to_date(i["date"], output_format='%Y-%m-%d %H:%M:%S')

        end = time()
        ex = end - start
        print("---------------------- trading data importers took  :", round(ex,3), " seconds ---------- ")
        return data

    def data_correction(self,trading_data, listing_data):
        # trading_data = self.get_trading_stats_by_collection(collection, interval)
        # listing_data = self.get_listing_stats_by_collection(collection, interval)
        i = 0
        while i < len(listing_data) and i < len(trading_data):
            if listing_data[i]['date'] != trading_data[i]["date"]:
                trading_data.insert(i, {"date": listing_data[i]["date"],
                                        "tr_count": trading_data[i]["tr_count"],
                                        "tr_count_change": 0,
                                        "tr_count_change_pct": 0,
                                        "tr_volume": trading_data[i]["tr_volume"],
                                        "tr_volume_change": 0,
                                        "tr_volume_change_pct": 0,
                                        "tr_min_price": trading_data[i]["tr_min_price"],
                                        "tr_min_price_change": 0,
                                        "tr_min_price_change_pct": 0,
                                        "tr_max_price": trading_data[i]["tr_max_price"],
                                        "tr_max_price_change": 0,
                                        "tr_max_price_change_pct": 0,
                                        "tr_avg_price": trading_data[i]["tr_avg_price"],
                                        "tr_avg_price_change": 0,
                                        "tr_avg_price_change_pct": 0})

            i = i + 1
        return 0

    def class_launcher(self, collection, interval):
        listing_data = self.get_listing_stats_by_collection(collection, interval)
        trading_data = self.get_trading_stats_by_collection(collection, interval)
        self.data_correction(trading_data=trading_data, listing_data=listing_data)
        return trading_data,listing_data

# d = TransactionsStatsRepository()
# trading_data,listing_data = d.class_launcher('DGOD',1440)
# print(len(trading_data))
# print(len(listing_data))
# print(trading_data[1])
# print("--------------------------------------------")
# print(listing_data[1])