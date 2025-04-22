class RiskManagement(object):

    @staticmethod
    def data_standardization(data, standardized_maxi):
        print(len(data))
        count = 0
        i = 0
        while i < len(data):
            if data[i]['ATR'] > standardized_maxi[i]:
                print(data[i]['date'])
                print(standardized_maxi[i])
                print(data[i]['ATR'])
                count = count+1
                print("*-*-*-*-*-*-**-*-*-*-*-*-**-*-*-*-*-*-**-*-*-*-*-*-*")
            i = i+1
        print(count)