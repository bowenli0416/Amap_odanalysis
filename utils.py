import pandas as pd

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

def wrongodlist():
    pass

if __name__ == "__main__":
    a = ['d70701297678984a952784242d36d287', '28967d62c78015ce18d2f935c29f9948']
    it = getuk_fl(a)
    for each in range(5):
            # print(iter(getuk_fl(['d70701297678984a952784242d36d287', '28967d62c78015ce18d2f935c29f9948'])).next())
            print(next(it))