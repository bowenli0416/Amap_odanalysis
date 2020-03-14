import pandas as pd
import csv
from odtime_generate.coor_transform import wgs84_to_gcj02

def getuk_fcsv(file):
    "get uk from csv"
    #TODO
    temp = pd.read_csv(file)
    for each in temp.iterrows():
        yield  each
def getuk_fl(uk_list):
    "get uk fromlist"
    for each in uk_list:
        yield each


def generate_odxy(file):
    #获得od上三角列表
    df = pd.read_excel(file).iloc[:, [-6,-2, -1]]
    df['Lng_hx'] = df.apply(lambda row: wgs84_to_gcj02(row['INSIDE_X'], row['INSIDE_Y'])[0], axis=1) #坐标转换
    df['Lat_hx'] = df.apply(lambda row: wgs84_to_gcj02(row['INSIDE_X'], row['INSIDE_Y'])[1], axis=1)
    print(df)
    df_c = df.copy(deep=True)
    i = 0
    for each1 in df.iterrows():
        df_c.drop([i], inplace=True)
        i += 1
        if i == len(df):
            break
        for each2 in df_c.iterrows():
            yield each1[1][3],each1[1][4],each2[1][3],each2[1][4],each1[1][0],each2[1][0]#the former 4 is the coordinates,
            #the last two is the value of index"[-6]",which is the t value.

class od():

    '''
    od表b数据结构
    '''
    def __init__(self, *args):
        self.output_dict = {}
        for each in args:
            args[each] = []
    def add(self,**kwargs):
        for key,value in kwargs.items():
            self.output_dict[key].append(value)
    def to_csv(self,file):
        pd.DataFrame(self.output_dict)
        return self.df.to_csv(file)




if __name__ == "__main__":
    file = '/Users/pro/Desktop/深圳1000网格的副本 2.xls'
    for each in generate_odxy(file):
        print(each)