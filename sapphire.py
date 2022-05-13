import requests
import csv
import pandas as pd
from tkinter import *
from pandastable import Table
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
from requests.api import get
import numpy as np
from ProxHunter import *


def get_proxies():
    with open('prox_container.csv', 'w',newline='') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerows(ProxyHunter().getallproxy())

def tracker(sub_total,ignore = []):

    proxies_list = [x[0] for x in csv.reader(open('prox_container.csv',"r")) if x[0] not in ignore]
    try:
        user_agent = UserAgent().random
        headers= {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
        proxy = {'https' if proxies_list[0][0].find('https')!=-1 else 'http':proxies_list[0]}
        coin_url = ','.join([x[0] for x in sub_total]) + ',BTC'
        url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(coin_url) 
        r = requests.get(url,headers=headers, proxies=proxy, timeout=5,verify=False)
        current_p = [[k,list(v.values())[0]] for k,v in r.json().items()]
        total = [sub_total[i]+[current_p[i][1]*float(sub_total[i][2])]+[current_p[i][1]*float(sub_total[i][2])-float(sub_total[i][1])] + [((current_p[i][1]*float(sub_total[i][2])-float(sub_total[i][1]))/float(sub_total[i][1]))*100] + [float(current_p[i][1])] 
        for i in range(len(sub_total)) if sub_total[i][0]==current_p[i][0]] + [['BTC',0,0,0,0,0,float(current_p[-1][1])]]
    except Exception:
        if len(proxies_list)==0:
            get_proxies()
        ignore.append(proxies_list[0])
        print(ignore)
        return([['loading'] + [1,1,1,1,1,1] for i in range(len([x for x in csv.reader(open('prox_container.csv',"r"))]))], ignore)
    return (total, ignore) 
   

class TestApp(Frame):

    d = dict()
    with open("CC_coins.csv", "r") as f:
        for i in csv.reader(f):
            if i[1] in d:
                d[i[1]] += np.fromiter(map(float, i[2:]), dtype = np.float64)
            else:
                d[i[1]] =  np.fromiter(map(float, i[2:]), dtype = np.float64) #.insert(0, )
   

    def __init__(self, parent=None):
        self.sub_total = [[i]+list(self.d[i]) for i in self.d]
        get_proxies()
        self.ignore = []
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('700x200')
        self.main.title('PnL')
        f = Frame(self.main)
        f.pack(fill="both",expand=True)
        total, self.ignore = tracker(self.sub_total, self.ignore)
        df = pd.DataFrame(total,columns=['СС','FP=' + str('%.0f' % sum([float(i[1]) for i in total])),'Q','CPQ='+str('%.0f' % sum([float(i[3]) for i in total])),str('%.1f' % sum([i[4] for i in total])) + ' +/-',str('%.1f' % ((sum([float(i[4]) for i in total])*100)/sum([float(i[1]) for i in total])) )+'%', 'PF1'])
        self.table = Table(f, dataframe=df)
        self.table.show()
        self.update_data()
        
        
    def update_data(self):
        total, self.ignore = tracker(self.sub_total, self.ignore)
        df = pd.DataFrame(total,columns=['СС','FP=' + str('%.0f' % sum([float(i[1]) for i in total])),'Q','CPQ='+str('%.0f' % sum([float(i[3]) for i in total])),str('%.1f' % sum([i[4] for i in total])) + ' +/-',str('%.1f' % ((sum([float(i[4]) for i in total])*100)/sum([float(i[1]) for i in total])) )+'%', 'PF1'])
        self.table.model.df = df
        self.table.redraw()
        self.after(1000,self.update_data)

app = TestApp()
app.mainloop()