from threading import Timer
import time as t
import pandas as pd
import requests
import datetime
import importlib, sys
# from retrying import  retry
import numpy as np
from odtime_generate import craw_exception as ce
from odtime_generate import utils as ut

class parse_url():

    def __init__(self,file,ukl,path,onum,dnum,url = 'https://restapi.amap.com/v3/direction/transit/integrated?origin={0},{1}'
                                         '&destination={2},{3}&city=0755&output=json&key={4}&strategy=0&nightflag=0'):
        '''

        :param file: file from ArcGIS
        :param userkey:
        :param url:
        :param path:存放结果csv文件的文件夹
        '''
        self.file = file
        self.url = url
        self.ukl = ukl
        self.path = path
        self.onum = onum
        self.dnum = dnum
        self.odwrongdic = ut.od('ox', 'oy', 'dx', 'dy', 'onum', 'dnum', 'type')

    def xy_generator(self):
        table = pd.read_excel(self.file).iloc[:, [-6, -2, -1]]
        for each in table.iterrows():
            yield each

    def get_odxy(self):
        #最后会形成完整的od表，但是计算次数太多，高德地图无法满足需求
        for oxy in self.xy_generator():
            for dxy in self.xy_generator():
                yield oxy,dxy


    def _parse_json(self,json):
        count = int(json['count'])
        if count != 0:
            # rc+=1;print(rc)
            duration = json['route']['transits']
            min_dur = np.inf
            for each in range(count):
                time = int(duration[each]['duration'])
                if time <= min_dur:
                    min_dur = time
                else:
                    continue
            return min_dur
        else:
            raise ce.NorouteException("there is no route ")

    # @retry(stop_max_attempt_number=8, wait_random_min=1000, wait_random_max=2000)
    def _get_json(self, url):
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()
            # if r.status_code ==200:
            #     return r.json()
            # else:
            #     raise ce.RequestatcodeException('REQUEST_STATUS_CODE_200_FAILED_ERROR')

    # @ut.count_func
    def parse_model(self):
        gen_od = 1
        gen_uk = 1
        time_mark = 0; error_breakmark = 0
        odg = ut.generate_odxy(self.file)
        ukg = self.ukl
        odg = ut.set_generator1(self.onum,self.dnum,odg)
        run_time = 0
        while True:
                try:
                    if gen_od == 1:
                        od = next(odg) #运行生成器
                        time_mark = 0
                    if gen_uk == 1:
                        user_key = next(ukg)
                    url = self.url.format(od[0],od[1],od[2],od[3],user_key)
                    json = self._get_json(url)#request 模块获得json
                    ce.analyse_statcode(json)# 分析status code
                except StopIteration as e:
                    print(e)
                    print('输出结束')
                    break
                except requests.exceptions.RequestException:
                    gen_uk = 0; gen_od = 0
                    time_mark += 1
                    print('网络链接出错，重试中...')
                    t.sleep(61)
                    if time_mark == 5: #多次循环后仍然报错，退出
                        if run_time == 0:
                            raise ce.CheckconnException("请检查连接后开始执行程序")
                        break # 多次循环后仍然报错直接退出
                    continue
                except ce.InvaluserkeyException as e:
                    gen_uk = 1; gen_od = 0; print(e)
                    continue #  the func continue to run
                except ce.DailyoverlimException as e:
                    gen_uk = 1; gen_od = 0; print(e)
                    continue
                except ce.TooFreqException as e:
                    t.sleep(61)
                    gen_uk = 0; gen_od = 0
                    continue
                except ce.MissReqParaException as e:
                    #代表坐标有误跨越了地区，所以缺失参数
                    self.odwrongdic.add(ox=od[0],oy=od[1],dx=od[2],dy=od[3],onum=od[4],dnum=od[5],type='mp')
                    gen_od = 1;gen_uk = 0
                    yield od[4], od[5], -1
                    continue
                except ce.OtherInfoCodeException as e:
                    gen_uk = 0;gen_od = 0
                    time_mark += 1
                    t.sleep(20);print('出现错误,重试中');print(e)
                    if time_mark == 5:  # 多次循环后仍然报错，进行下次循环
                        print(e)#打印错误
                        break
                    continue
                else: #if no exception has been caught
                    try:
                        gen_od = 1; gen_uk = 0
                        min_dur = self._parse_json(json)
                        if run_time % 100 ==0:
                            print('执行了：{0}次'.format(run_time))
                        run_time+=1
                    except ce.NorouteException as e:
                        min_dur = np.inf
                    except Exception as e:  #unkown excep
                        print(json)
                        print("未知错误："+e)
                        break
                yield od[4], od[5], min_dur


if __name__ == "__main__":

    user_key = 'd70701297678984a952784242d36d287'
    file = '/Users/pro/Desktop/深圳1000网格的副本.xls'
    ag = parse_url(file,user_key)
    for each in ag.request_model():
        print(each)
