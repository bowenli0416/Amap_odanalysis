from odtime_generate.parse_url import *
from odtime_generate import utils as ut
import pandas as pd

def run_test(file,ukl):
    PU = parse_url(file,ukl)
    odgen = PU.parse_model()
    for each in odgen:
        print(each)

def run(file, ukl, path):
    pu = parse_url(file, ukl, path)
    odtable = ut.od('onum','dnum','min_dur')
    odgen = pu.parse_model()
    for each in odgen:
        odtable.add(onum=each[0],dnum=each[1],min_dur=each[2])
    temp = odtable.output_dict['onum']; temp1 = odtable.output_dict['dnum']
    if len(temp)!=0:
        lasto = temp[-1]
        lastd = temp1[-1]
        pu.odwrongdic.to_csv('./wrongodfile/wrongod.csv')
        odtable.to_csv(path + r'/{0}_{1}.csv'.format(int(lasto), int(lastd)))
    else:
        pu.odwrongdic.to_csv('./wrongodfile/wrongod.csv')
        odtable.to_csv(path + r'/{0}_{1}.csv'.format(0, 0))

if __name__ == "__main__":
    ukl = ['d70701297678984a952784242d36d287', 'a54dedbe29cfc92eff676412907f7f39']
    file = './datdemo/深圳1000网格的副本.xls'
    path = r'./csvfile'
    ituk = ut.getuk_fl(ukl)
    run(file,ituk,path)