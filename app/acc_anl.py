# coding: UTF-8

import pandas as pd
import sys
import re
import datetime
import os
import glob
import matplotlib as mpl
import matplotlib
import matplotlib.pyplot as plt
import pyodbc
import gc
from dotenv import load_dotenv


#import japanize_matplotlib

load_dotenv()
data_dir = os.environ['DATA_DIR']
exbt_list_filenmae = os.environ['EXBT_LIST_FILENAME']


plt.style.use('ggplot') 
font = {'family' : 'meiryo'}
matplotlib.rc('font', **font)

d_list = glob.glob('data\\YBIZ_c_*.csv')
d_list.sort()

sum_df = pd.DataFrame()
for d in d_list:
    print(d)
    dt = re.search('[0-9\-]+',d).group()
    df = pd.read_csv(d,encoding="cp932")
#    df = pd.read_csv(d)
    df['日付'] = dt
    df['アクセス増分'] = 0
    df['アクセス累計'] = 0
#    df['アクセス数'] = df['アクセス数']
    df['ウォッチ増分'] = 0
    df['ウォッチ累計'] = 0
#    df['ウォッチ数'] = df['ウォッチ数'])
    df['MAアクセス増分'] = 0
    df['MAウォッチ増分'] = 0
    df['データ数'] = 0
    sum_df = sum_df.append(df)

#sum_df['データ数'] = 0


sys.exit()


del df

last_df = pd.DataFrame()
k_set = set(sum_df['管理番号'])

#sys.exit()

#-----在庫ありの管理番号集合を候補とするロジック追加-------


#conn_str = (
#    r'DRIVER={Microsoft Access Driver (*.mdb)};'
#    r'DBQ=s:\@aaaaa\db2_be.mdb;'
#    )

#--21/09/23---

conn_str = (
    r'Driver={MySQL ODBC 8.0 Unicode Driver};'
    r'Server=hksagri;Database=hksdb;UID=hikousen;PWD=rs151000'
)

cnxn = pyodbc.connect(conn_str)




p_df = pd.read_sql(sql="SELECT * FROM 商品マスタ where 在庫数量>0 ", con=cnxn)

#print(p_df)

k_set = k_set & set(p_df['コード'])

del p_df

print(k_set)

#----------------------------------

k_l = list(k_set)
for k in k_l:
    k_df = sum_df[sum_df['管理番号']==k].copy()
    #k_df = sum_df[sum_df['管理番号']==k]
    k_df.sort_values('日付')
    k_df.reset_index(inplace=True)
#    print (k_df)
    o_ac = int(k_df.iloc[0]['アクセス数'])
    o_wc = int(k_df.iloc[0]['ウォッチ数'])
    sum_ac = o_ac
    sum_wc = o_wc
#    last_ac = 0
#    last_wc = 0
#    last_price = 0
#    last_date = ''
    last_idx =0
    for idx,row in k_df.iterrows():
#        n_ac = int(row['アクセス数'].replace(',',''))
#        n_wc = int(row['ウォッチ数'].replace(',',''))
        n_ac = int(row['アクセス数'])
        n_wc = int(row['ウォッチ数'])
        #---アクセス正規化----
        dt_ac =n_ac - o_ac
        if dt_ac < 0 :
            dt_ac = n_ac
        k_df.at[idx,'アクセス増分'] = dt_ac
        sum_ac += dt_ac
        k_df.at[idx,'アクセス累計'] += sum_ac
        o_ac = n_ac
        #---ウォッチ正規化----
        dt_wc =n_wc - o_wc
        #if dt_wc < 0 :
        #    dt_wc = n_wc
        k_df.at[idx,'ウォッチ増分'] = dt_wc
        sum_wc += dt_wc
        k_df.at[idx,'ウォッチ累計'] += sum_wc
        o_wc = n_wc
        k_df.at[idx,'データ数'] = idx+1
        last_idx = idx
#        last_ac = n_ac
#        last_wc = n_wc
    #        last_price = k_df.at[idx,'現在価格']
#        last_date = k_df.at[idx,'日付']
#    last_df = last_df.append(k_df.loc[last_idx])
    k_df['MAアクセス増分'] = k_df['アクセス増分'].rolling(3).mean()
    k_df['MAウォッチ増分'] = k_df['ウォッチ増分'].rolling(3).mean()
    last_df = last_df.append(k_df.loc[last_idx])

    #print(k_df[['管理番号','日付','アクセス数','ウォッチ数','アクセス増分','アクセス累計','ウォッチ増分','ウォッチ累計','現在価格','データ数']])
    #g_df = k_df[['日付','アクセス増分','MAアクセス増分','アクセス累計','ウォッチ増分','MAウォッチ増分','ウォッチ累計','現在価格']]
    print(k_df.tail(1))    
#    g_df['ウォッチ累計'] = g_df['ウォッチ累計']*10
    try:
#        ax = g_df.plot(title=k+row['タイトル'],x='日付',secondary_y=['アクセス累計'],figsize=(9,7),rot=45)
#        ax.set_ylabel('ウォッチ累計',rotation=0)
#        ax.right_ax.set_ylabel('アクセス累計',rotation=0)
#        ax = g_df.plot(subplots=True,title=k+row['タイトル'],x='日付',figsize=(9,14),rot=45,sharex=True)
#        fig = plt.gcf()

#    g_df = df[['日付','アクセス増分','AC移動平均','アクセス累計','ウォッチ増分','WT移動平均','ウォッチ累計','現在価格']]
    
    
        #fig, axes = plt.subplots(5,1,figsize=(8, 10), sharex=True)

        #tt = row['タイトル']
        #fig.suptitle(k+' '+':'.join(tt.split(':')[:5]))

        #g_df.plot(x='日付',y=['アクセス増分','MAアクセス増分'],ax=axes[0],rot=45)
        #g_df.plot(x='日付',y='アクセス累計',ax=axes[1],rot=45)
        #g_df.plot(x='日付',y=['ウォッチ増分','MAウォッチ増分'],ax=axes[2],rot=45,color=['#348ABD', '#7A68A6'])
        #g_df.plot(x='日付',y='ウォッチ累計',ax=axes[3],rot=45)
        #g_df.plot(x='日付',y='現在価格',ax=axes[4],rot=45)


        
        #fig.savefig('graph\\anl_'+k+'.png')
        #plt.cla()
        #plt.clf()
        #plt.close('all')
        k_df.to_csv('graph\\anl_'+k+'.csv', encoding='cp932')
    except Exception as e:
        print("*************plotエラー:******************",k,e)

    del k_df
    #del g_df
    gc.collect()


last_df.to_csv('last_sum\\last_sum_'+str(datetime.date.today())+'.csv',encoding='cp932')

#plt.show()
#plt.close()

