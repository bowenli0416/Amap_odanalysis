from threading import Timer
import time
import pandas as pd
import requests
import datetime
import importlib, sys
import numpy as np
from odtime_generate.craw_exception import *
from retrying import retry

#TODO sleepfunc  retryfunc are needed

def userkeylist():
    pass

class amap_generate():

    def __init__(self,file,userkey,url = 'https://restapi.amap.com/v3/direction/transit/integrated?origin={0},{1}'
                                         '&destination={2},{3}&city=0755&output=json&key={4}&strategy=0&nightflag=0'):
        '''

        :param file: file from ArcGIS
        :param userkey:
        :param url:
        '''
        self.file = file
        self.userkey = userkey
        self.url = url
    def xy_generator(self):
        table = pd.read_excel(self.file).iloc[:, [-6, -2, -1]]
        for each in table.iterrows():
            yield each

    def get_odxy(self):
        #最后会形成完整的od表，但是计算次数太多，高德地图无法满足需求
        for oxy in self.xy_generator():
            for dxy in self.xy_generator():
                yield oxy,dxy

    def _generate_odxy(self):
        #获得od上三角列表
        df = pd.read_excel(self.file).iloc[:, [-6,-2, -1]]
        df_c = df.copy(deep=True)
        i = 0
        for each1 in df.iterrows():
            df_c.drop([i], inplace=True)
            i += 1
            if i == len(df):
                break
            for each2 in df_c.iterrows():
                yield each1[1][1],each1[1][2],each2[1][1],each2[1][2],each1[1][0],each2[1][0]#the former 4 is the coordinates,
                #the last two is the value of index"[-6]",which is the t value.


    def _get_url(self,url):

            r = requests.get(url,timeout=30)

            if r.status_code ==200:
                return r.json()
            else:
                raise Exception('REQUEST_STATUS_CODE_200_FAILED_ERROR')#may be a raise senten will be better


    def _analyse_statcode(self,json):
        stat_code = json['status']
        if stat_code == 0:
            # only if failed, can a info_code be generated
            info_code = json['info']
            if info_code == 1001:
                raise Exception('INVALID_USER_KEY_ERROR')
            if info_code == 10003:
                raise  Exception('DAILY_QUERY_OVER_LIMIT_ERROR')
            if info_code == 10004:
                raise Exception('ACCESS_TOO_FREQUENT_ERROR')

        else:
            return json

    def request_model(self):

            for od in self._generate_odxy():

                    url = self.url.format(od[0],od[1],od[2],od[3],self.userkey)
                    try:
                        json = self._get_url(url)#get the json

                        self._analyse_statcode(json)
                    except Exception as e:
                        print(e) #TODO

                    except UserkeyException as e:
                        pass

                    else: #if no exception has been caught
                        count = int(json['count'])
                        if count != 0:
                            duration = json['route']['transits']
                            min_dur = np.inf
                            for each in range(count):
                                time = int(duration[each]['duration'])
                                if time <= min_dur:
                                    min_dur = time
                                else:
                                    continue
                        else:
                            raise Exception("there is no route ")
                    yield dict(t='{0}{1}'.format(od[4],od[5]),time=min_dur)


if __name__ == "__main__":
    # origin_x = 114.291689
    # origin_y = 22.749781
    # destination_x = 114.041092
    # destination_y = 22.637029
    # city = '深圳'
    # user_key = 'd70701297678984a952784242d36d287'
    # url = 'https://restapi.amap.com/v3/direction/transit/integrated?origin=' \
    #       '{0},{1}&destination={2},{3}&city={4}&output=json&key={5}&strategy=0&nightflag=0'
    # user_url = url.format(origin_x,origin_y,destination_x,destination_y,city,user_key)
    # r = requests.get(user_url)
    # print(r.json())

   #
    user_key = 'd70701297678984a952784242d36d287'
    file = '/Users/pro/Desktop/深圳1000网格的副本.xls'
    ag = amap_generate(file,user_key)
    for each in ag.request_model():
        print(each)
