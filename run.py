from odtime_generate.parse_url import *
from odtime_generate import utils as ut
import pandas as pd
import numpy as np

def run_test(file,ukl):
    PU = parse_url(file,ukl)
    odgen = PU.parse_model()
    for each in odgen:
        print(each)

def run(file, ukl, path,path1):
    odwrongfilenum = ut.check_csv1(path1)[0]
    # odtable = ut.od('onum','dnum','min_dur')
    odtable, sonum, sdnum = ut.genrate_odmatrix(file,path)
    fonum, fdnum = [0], [0]
    pu = parse_url(file, ukl, path,sonum,sdnum)
    odgen = pu.parse_model()
    for each in odgen:
        odtable[int(each[0])][int(each[1])] = each[2]
        fonum[0] = each[0]
        fdnum[0] = each[1]
        # odtable.add(onum=each[0],dnum=each[1],min_dur=each[2])
    # temp = odtable.output_dict['onum']; temp1 = odtable.output_dict['dnum']
    # if len(temp)!=0:
    #     lasto = temp[-1]
    #     lastd = temp1[-1]
    #     pu.odwrongdic.to_csv(path1+'/wrongod{0}.csv'.format(odwrongfilenum))
    #     odtable.to_csv(path + r'/{0}_{1}.csv'.format(int(lasto), int(lastd)))
    # else:
    #     pu.odwrongdic.to_csv(path1+'/wrongod{0}.csv'.format(odwrongfilenum))
    #     odtable.to_csv(path + r'/{0}_{1}.csv'.format(0, 0))
    ut.del_files(path)#存在bug
    np.save(path + r'/{0}_{1}.npy'.format(int(fonum[0]),int(fdnum[0])),odtable)
    pu.odwrongdic.to_csv(path1 + '/wrongod{0}.csv'.format(odwrongfilenum))
if __name__ == "__main__":
    ukl = ['d70701297678984a952784242d36d287', 'a54dedbe29cfc92eff676412907f7f39']
    file = './datdemo/深圳1000网格.xls'
    path = r'./csvfile'
    path1 = r'./wrongodfile'
    ituk = ut.getuk_fl(ukl)
    run(file,ituk,path,path1)