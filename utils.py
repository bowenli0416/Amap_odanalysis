import pandas as pd
import os
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
def check_csv(path):
    '''
    检查csvfile中的文件，确定生成器的开始位置
    '''
    sortdict = {}
    for each in os.listdir(path):
        to = int(each[0]); td = int(each[2])
        if to in sortdict:
            if sortdict[to] < td:
                sortdict[to] = td
            else:
                continue
        else:
            sortdict[to] = td
    if len(sortdict) != 0:
        maxo = sorted(sortdict)[-1]
        return maxo,sortdict[maxo]
    else:
        print("csvfile中不存在csv文件")
        return  0,0

def set_generator(path,odgenertor):
    """
    设置生成器确保生成器接着已有文件继续生成
    """
    onum,dnum = check_csv(path)
    if onum == 0  and dnum == 0:
        return odgenertor
    else:
        while True:
            od = next(odgenertor)
            if od[4]==onum and od[5] == dnum:
                return odgenertor

def generate_odxy(file):
    #获得od上三角列表
    df = pd.read_excel(file).iloc[:, [-6,-2, -1]]
    df['Lng_hx'] = df.apply(lambda row: wgs84_to_gcj02(row['INSIDE_X'], row['INSIDE_Y'])[0], axis=1) #坐标转换
    df['Lat_hx'] = df.apply(lambda row: wgs84_to_gcj02(row['INSIDE_X'], row['INSIDE_Y'])[1], axis=1)
    # print(df)#打印校正前后的坐标
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
    od表数据结构
    '''
    def __init__(self, *args):
        self.output_dict = {}
        for each in args:
            self.output_dict[each] = []
    def add(self,**kwargs):
        try:
            for key,value in kwargs.items():
                self.output_dict[key].append(value)
        except Exception as e:
            print("OD属性字段有误")
    def to_csv(self,file):
        df = pd.DataFrame(self.output_dict)
        return df.to_csv(file)




if __name__ == "__main__":
    path = r'./csvfile'
    # print(check_csv(path))
    file = './datdemo/深圳1000网格的副本.xls'
    G = generate_odxy(file)
    G = set_generator(path, G)
    while True:
        od = next(G)
        print(od[4],od[5])