from threading import Timer
import time as t
import pandas as pd
import requests
import datetime
import importlib, sys
import numpy as np
from odtime_generate import craw_exception as ce
from odtime_generate import utils as ut

#TODO sleepfunc  retryfunc are needed


class parse_url():

    def __init__(self,file,ukl,url = 'https://restapi.amap.com/v3/direction/transit/integrated?origin={0},{1}'
                                         '&destination={2},{3}&city=0755&output=json&key={4}&strategy=0&nightflag=0'):
        '''

        :param file: file from ArcGIS
        :param userkey:
        :param url:
        '''
        self.file = file
        self.url = url
        self.ukl = ukl

    def xy_generator(self):
        table = pd.read_excel(self.file).iloc[:, [-6, -2, -1]]
        for each in table.iterrows():
            yield each

    def get_odxy(self):
        #最后会形成完整的od表，但是计算次数太多，高德地图无法满足需求
        for oxy in self.xy_generator():
            for dxy in self.xy_generator():
                yield oxy,dxy




    def _get_json(self,url):


            r = requests.get(url,timeout=30)

            if r.status_code ==200:
                return r.json()
            else:
                raise ce.RequestatcodeException('REQUEST_STATUS_CODE_200_FAILED_ERROR')


    def parse_model(self):
        # user_key = next(self.ukl)
        # for od in self._generate_odxy():
        gen_od = 1
        gen_uk = 1
        time_mark = 0
        odg = ut.generate_odxy(self.file)
        ukg = self.ukl
        rc = 0
        while True:
                try:
                    if gen_od == 1:
                        od = next(odg)
                        time_mark = 0
                    if gen_uk == 1:
                        user_key = next(ukg)
                    url = self.url.format(od[0],od[1],od[2],od[3],user_key)
                    json = self._get_json(url)#get the json
                    ce.analyse_statcode(json)
                except StopIteration as e:
                    print('the output is done')
                    break
                except ce.RequestatcodeException as e:
                    gen_uk = 0; gen_od = 0
                    time_mark+=1
                    if time_mark == 5:
                        gen_uk = 0; gen_od = 1
                        ut.wrongodlist()
                except ce.InvaluserkeyException as e:
                    gen_uk = 1; gen_od = 0
                    continue #  the func continue to run
                except ce.DailyoverlimException as e:
                    gen_uk = 1;gen_od = 0
                    continue
                except ce.TooFreqException as e:
                    t.sleep(60)
                    gen_uk = 0; gen_od = 0
                    continue
                except ce.MissReqParaException as e:
                    #means the coord is wrong , for now just continue
                    continue
                else: #if no exception has been caught
                    try:
                        gen_od = 1; gen_uk = 0
                        count = int(json['count'])
                        if count != 0:
                            rc+=1;print(rc)
                            duration = json['route']['transits']
                            min_dur = np.inf
                            for each in range(count):
                                time = int(duration[each]['duration'])
                                if time <= min_dur:
                                    min_dur = time
                                else:
                                    continue
                        else:
                            raise ce.NorouteException("there is no route ")
                    except ce.NorouteException as e:
                        min_dur = np.inf
                        print(e)
                    except Exception as e:
                        #unkown excep
                        print(json)
                        break
                # yield dict(t='{0}{1}'.format(od[4],od[5]),time=min_dur)
                yield  od[4],od[5],min_dur


if __name__ == "__main__":

    user_key = 'd70701297678984a952784242d36d287'
    file = '/Users/pro/Desktop/深圳1000网格的副本.xls'
    ag = parse_url(file,user_key)
    for each in ag.request_model():
        print(each)
