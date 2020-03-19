import pandas as pd
import os
from odtime_generate.coor_transform import wgs84_to_gcj02
import re
import numpy as np
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
        temp = re.findall(r'\d+', each)
        to = int(temp[0]); td = int(temp[1])
        if to in sortdict:
            if sortdict[to] < td:
                sortdict[to] = td
            else:
                continue
        else:
            sortdict[to] = td
    if len(sortdict) != 0:
        maxo = sorted(sortdict)[-1]
        return maxo, sortdict[maxo]
    else:
        print("csvfile中不存在csv文件")
        return  0,0

def check_csv1(path):
    '''
    检查wrongodfile中是否有文件
    '''
    file_list = []
    for each in os.listdir(path):
        file_list.append(each)
    lf = len(file_list)
    if lf != 0:
        file = file_list[0]
        return len(file_list), file_list[0]
    else:
        return 0,'0'
def set_generator(path,odgenertor):
    """
    设置生成器确保生成器接着已有文件继续生成 此模块针对需要生成odcsv
    """
    onum, dnum = check_csv(path)
    if onum == 0  and dnum == 0:
        return odgenertor
    else:
        while True:
            od = next(odgenertor)
            if od[4]==onum and od[5] == dnum:
                return odgenertor

def set_generator1(onum,dnum,odgenerator):
    '''此模块针对生成odmatrix'''

    onum, dnum = onum, dnum
    if onum == 0  and dnum == 0:
        return odgenerator
    else:
        while True:
            od = next(odgenerator)
            if od[4] == onum and od[5] == dnum:
                return odgenerator



def genrate_odmatrix(file,path):
    '''
    得出全零方阵
    '''
    length,file_name = check_csv1(path)
    if length == 0:#文件夹中没有文件
        df = pd.read_excel(file)
        s = (len(df),len(df))
        odmat = np.zeros(s)
        onum = 0; dnum = 0
    else:
        file_path = path + '\\'+ file_name
        odmat = np.load(file_path)
        temp = re.findall(r'\d+', file_name)
        onum = int(temp[0]); dnum = int(temp[1])

    return odmat, onum, dnum


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

def del_files(path):
    '''
    对应文件夹中只能有一个npy文件
    '''
    for each in os.listdir(path):
        path_file = os.path.join(path,each)
        os.remove(path_file)

# def count_func(func):
#     """
#     装饰器计算函数执行次数
#     """
#     num = 0
#     def inner_func(self,*args,**kwargs):
#         func(self,*args,**kwargs)
#         print(self)
#         nonlocal num
#         num+=1
#         if num%20==0:
#             print('函数执行了{0}'.format(num))
#     return inner_func

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
    # path = r'./csvfile'
    # print(check_csv(path))
    # file = './datdemo/深圳1000网格的副本.xls'
    # G = generate_odxy(file)
    # G = set_generator(path, G)
    # while True:
    #     od = next(G)
    #     print(od[4],od[5])
    path = r'./wrongodfile'
    print(check_csv1(path))