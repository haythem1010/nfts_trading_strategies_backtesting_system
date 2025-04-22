from pprint import pprint
import requests as req
import utils.helpers as hlp
import pymysql
from utils.consts import DATABASE_CONFIG


"""
        # collection must be one of the following values:
        #   "aidegens, AUROR, BSL, BORYOKU, BGB, CWM, CoC, DAPE,
        #   "DEGG, DFC, FFF, FRTS, GGSG, GENOPET, GD, MIDH, Nyan, C3, ,
        #   "okay_bears, PRTL, PRIM, QT, SSC, SMB, SAC, taiyo_robotics,
        #   " OMNI, TAT, DGOD, C3L"

"""

class CollectionsByAPI(object):

    trading_stats_url = f"https://be.suipa.xyz/transaction_stat/trading"
    # listing_stats = f"https://be.suipa.xyz/listing/stat"
    listing_stats_url = f"https://be.suipa.xyz/transaction_stat/listing"


    @staticmethod
    def get_all_collections():
        """
        :return: list of all collections available in the server
        """

        url = f"https://be.suipa.xyz/transactions/all_collections/stats"
        resp = req.get(url)
        collections = []
        if resp.status_code == 200:
            collections = resp.json()
        else:
            print("ERROR")

        names = []
        for i in collections:
            names.append(i["collection"])
        names = hlp.delete_duplicates(names)
        # pprint(len(names))
        # pprint(names)
        return names

    @staticmethod
    def get_available_collections(local_data=False):
        names = []
        if not local_data:
            url = f"https://be.suipa.xyz/transaction_stat/for_analysis"
            resp = req.get(url)
            collections = []
            if resp.status_code == 200:
                collections = resp.json()
            else:
                print("ERROR")

            for i in collections:
                names.append(i["collection"])
        else:
            names = ['aidegens', 'AUROR', 'BSL', 'BORYOKU', 'BGB', 'CWM', 'CoC', 'DAPE', 'DEGG', 'DFC', 'FFF',
                     'FRTS', 'GGSG', 'GENOPET', 'GD', 'MIDH', 'Nyan', 'C3', 'okay_bears',
                     'PRTL', 'PRIM', 'QT', 'SSC', 'SMB', 'SAC', 'taiyo_robotics', 'OMNI', 'TAT', 'DGOD', 'C3L']
        return names



    def check_stats(self, timeframe):

        mylist = self.get_available_collections()
        copy_of_list = []
        for i in mylist:
            url = self.trading_stats_url + f"/{i}/{str(timeframe)}"
            resp = req.get(url=url)
            if resp.status_code == 200:
                copy_of_list.append(i)

        return copy_of_list


    def get_transactions_stats_available(self, collection, duration):
        url = self.trading_stats_url + f"/{collection}/{str(duration)}"
        resp = req.get(url=url)
        data = []
        if resp.status_code == 200:
            data = resp.json()
        else:
             print("Error : ", resp.status_code)

        for i in data:
            i["date"] = hlp.convert_timestamp_to_date(i["date"], output_format='%Y-%m-%d %H:%M:%S')
        return data


    def get_listing_data_stats_available(self, collection, duration):
        url = self.listing_stats_url+f"/{collection}/{str(duration)}"
        resp = req.get(url)
        data = []
        if resp.status_code == 200:
            data = resp.json()
        else:
            print("ERROR : ", resp.status_code)

        for i in data:
            i["date"] = hlp.convert_timestamp_to_date(i["date"], output_format='%Y-%m-%d %H:%M:%S')
        return data

    def trading_data_correction(self, collection, window, listing_data):
        trading_data = self.get_transactions_stats_available(collection, window*1440)
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
        # pprint(trading_data)
        # pprint(listing_data)

        return trading_data



#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

class CollectionsBySQL(object):
    base = DATABASE_CONFIG()

    def available_collections_query(self):
        cnx = pymysql.connect(user=self.base.USER,
                                  password=self.base.PWD,
                                  host=self.base.HOST,
                                  database=self.base.NAME,
                                  port=self.base.PORT
                                  )
        cur = cnx.cursor()
        query = 'SELECT collection FROM transaction_stat GROUP BY 1'
        cur.execute(query)
        collections = cur.fetchall()
        for row in cur:
            print(row)

        cur.close()
        cnx.close()

        return collections


# col = CollectionsByAPI()
# coll = col.get_listing_data_stats_available("DGOD",1)
