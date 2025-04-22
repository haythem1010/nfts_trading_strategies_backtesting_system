# from pprint import pprint
# import requests as req
#
#
# class DataImporters(object):
#
#     source = f"https://be.suipa.xyz/transaction_stat/trading"
#
#     def get_numeric_data(self, collection, timeframe):
#         url = self.source + f"/{collection}/{str(timeframe)}"
#         resp = req.get(url=url)
#         data = []
#         if resp.status_code == 200:
#             data = resp.json()
#         else:
#             print("Error : ", resp.status_code)
#         pprint(data)
#         return data

