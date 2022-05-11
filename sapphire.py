# from numpy import ubyte
import requests
import csv
import pandas as pd
from tkinter import *
from pandastable import Table
import pprint
# from typing import Counter
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
# from IPython.core.display import clear_output
from requests.api import get
import numpy as np

# import main
# import random

user_agent_list = (
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
)

# coins = pd.DataFrame([x[1:] for x in csv.reader(open("CC_coins.csv","r"))]).groupby(0).aggregate(lambda x: list(x)).reset_index().values.tolist()
# print(coins)
# sub_total = [[coins[i][0], sum([float(j) for j in coins[i][1]]), sum([float(j) for j in coins[i][2]])] for i in range(len(coins))]
# print(sub_total)

d = dict()
with open("CC_coins.csv", "r") as f:
# with open(r'/home/makbuk/dev/PnL_CC/finace_management/Vovak.csv', "r") as f:

    for i in csv.reader(f):
        if i[1] in d:
            d[i[1]] += np.fromiter(map(float, i[2:]), dtype = np.float64)
            # print(type(np.fromiter(map(float, i[2:]), dtype = np.float64)))
        else:
            d[i[1]] =  np.fromiter(map(float, i[2:]), dtype = np.float64) #.insert(0, )

sub_total = [[i]+list(d[i]) for i in d]

# pd.DataFrame(d).T.values.tolist()#.pivot_table(index="n", columns="Therapy", values="expr"))
# print(sub_total)


ua = UserAgent()

def get_prox():
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    
    proxies_list = []

    for table in soup.find_all('table'):
        try:    
            if 'table-striped' in table['class']:
                proxies_list =  [i for i in [i.text for i in table.find_all('td')] if all(x.isdigit() for x in i.split('.'))]
                # print(proxies_list)
        except KeyError:
            pass
    
    new_proxies = [proxies_list[i:i+2] for i in range(0,len(proxies_list),2)]#получили лист проксей

    df_container = pd.DataFrame([i for i in new_proxies if i[0] not in [x[1] for x in csv.reader(open('prox_container.csv',"r"))]])#если новые, то добавили
    
    with open('prox_container.csv','a', newline='', errors = 'ignore') as f:
        pd.concat([df_container]).to_csv(f, header = False)

CC_cash =[sub_total[i] + [0,0,0,0] for i in range(len(sub_total))]
def tracker(ignore = []):

    proxies_list = [x[1::] for x in csv.reader(open('prox_container.csv',"r")) if x[1] not in ignore][::-1]
    # print('proxies_list', proxies_list)
    try:
        user_agent = random.choice(user_agent_list)
        headers= {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
        proxy = {"https": 'https://'+ proxies_list[0][0] + ':' + proxies_list[0][1], "http": 'https://'+ proxies_list[0][0] + ':' + proxies_list[0][1]}
        # print('current_proxy: ',proxy)
    
        coin_url = ','.join([x[0] for x in sub_total]) + ',BTC'
        url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(coin_url) 
        # r = requests.get(url,headers=headers, proxies=proxy, timeout=5,verify=False)
        r = requests.get(url,headers=headers)

        #print(requests.get('https://httpbin.org/ip', proxies=proxy))
        # pprint.pprint(r.json())
        current_p = [[k,list(v.values())[0]] for k,v in r.json().items()]
        # print(current_p)
        
        total = [sub_total[i]+[current_p[i][1]*float(sub_total[i][2])]+[current_p[i][1]*float(sub_total[i][2])-float(sub_total[i][1])] + [((current_p[i][1]*float(sub_total[i][2])-float(sub_total[i][1]))/float(sub_total[i][1]))*100] + [float(current_p[i][1])] 
        for i in range(len(sub_total)) if sub_total[i][0]==current_p[i][0]] +[['BTC',0,0,0,0,0,float(current_p[-1][1])]]
        # print(total)
    except (AttributeError,requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout,requests.exceptions.ReadTimeout, IndexError):
        # json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        ignore.append(proxies_list[0][0])
        # print('ignore', ignore)
        global CC_cash
        get_prox()
        return(CC_cash, ignore)
    CC_cash = total
    return (total, ignore) 
   

class TestApp(Frame):

    def __init__(self, parent=None):
        get_prox()
        self.ignore = []
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        # self.main.geometry('600x200')
        self.main.title('PnL')
        f = Frame(self.main)
        f.pack(fill="both",expand=True)
        # f.grid()
        total, self.ignore = tracker(self.ignore)
        df = pd.DataFrame(total,columns=['СС','FP=' + str('%.0f' % sum([float(i[1]) for i in total])),'Q','CPQ='+str('%.0f' % sum([float(i[3]) for i in total])),str('%.1f' % sum([i[4] for i in total])) + ' +/-',str('%.1f' % ((sum([float(i[4]) for i in total])*100)/sum([float(i[1]) for i in total])) )+'%', 'PF1'])
        self.table = Table(f, dataframe=df)
        self.table.show()
        self.update_data()
        
        
    def update_data(self):
        # self.tracker = tracker()
        total, self.ignore = tracker(self.ignore)
        df = pd.DataFrame(total,columns=['СС','FP=' + str('%.0f' % sum([float(i[1]) for i in total])),'Q','CPQ='+str('%.0f' % sum([float(i[3]) for i in total])),str('%.1f' % sum([i[4] for i in total])) + ' +/-',str('%.1f' % ((sum([float(i[4]) for i in total])*100)/sum([float(i[1]) for i in total])) )+'%', 'PF1'])
        self.table.model.df = df
        self.table.redraw()
        # self.table.grid_remove()
        # self.table.grid()
        # self.pack(fill="both",expand=True)
        self.after(1000,self.update_data)

app = TestApp()
app.mainloop()