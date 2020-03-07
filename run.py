from odtime_generate.parse_url import *
from odtime_generate import utils as ut
import pandas as pd

def run(file,ukl):


    PU = parse_url(file,ukl)
    odgen = PU.parse_model()
    for each in odgen:
        print(each)

def output(file,ukl):
    output_dic = dict(onum=[],dnum=[],time=[])
    PU = parse_url(file, ukl)
    odgen = PU.parse_model()
    for each in odgen:
        output_dic['onum'].append(each[0])
        output_dic['dnum'].append(each[1])
        output_dic['time'].append(each[2])
    lasto = output_dic['onum'][-1]
    lastd = output_dic['dnum'][-1]
    df = pd.DataFrame(output_dic)

    return df.to_csv(r'./{0}_{1}.csv'.format(lasto,lastd))

if __name__ == "__main__":
    ukl = ['d70701297678984a952784242d36d287', '28967d62c78015ce18d2f935c29f9948']
    file = '/Users/pro/Desktop/深圳1000网格1.xls'
    ituk = ut.getuk_fl(ukl)
    output(file,ituk)