# from numpy import ubyte
import requests
import csv
import pandas as pd
from tkinter import *
from pandastable import Table
# import pprint
# import main
# import random

coins = [x[1:] for x in csv.reader(open("C:\\it\\sapphire\\CC_coins.csv","r"))]
# print(coins)
dups = [coins[i:i+2] for i in range(len(coins)-1) if coins[i][0] == coins[i+1][0]]
# print(dups)
sumarized_dupes = []
for i in dups:
    calculate_usd = 0
    calculate_tok = 0
    for j in i:
        token_name = j[0]
        calculate_usd +=float(j[1]) 
        calculate_tok +=float(j[2])
    sumarized_dupes.append([token_name,calculate_usd,calculate_tok])
# print(sumarized_dupes)
sub_total = [x for x in coins if x not in [x for xs in dups for x in xs]] + sumarized_dupes

# print(coins_sumarized_dupes)
# print(pd.DataFrame(sub_total,columns=['СС','FP','Quantity']))

def tracker():

    coin_url = ','.join([x[0] for x in sub_total])
    url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(coin_url)
    r = requests.get(url)
    # print(r.status_code)
    # pprint.pprint(r.json())
    # print(r.status_code)
    # pprint.pprint(r.json())

    current_p = [[k,list(v.values())[0]] for k,v in r.json().items()]
    # print(current_p)

    total = [sub_total[i]+[current_p[i][1]*float(sub_total[i][2])]+[current_p[i][1]*float(sub_total[i][2])-float(sub_total[i][1])] + [((current_p[i][1]*float(sub_total[i][2])-float(sub_total[i][1]))/float(sub_total[i][1]))*100] for i in range(len(current_p)) if sub_total[i][0]==current_p[i][0]]
    # print(pd.DataFrame(total,columns=['СС','FP','Q','CP(1)*Q',str(sum([i[4] for i in total]))[:4] + '+/- ' ,'%']))
    
    return total 
    

class TestApp(Frame):

        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            # self.main.geometry('600x200')
            self.main.title('PnL')
            f = Frame(self.main)
            f.pack(fill="both",expand=True)
            # f.grid()
            df = pd.DataFrame(tracker(),columns=['СС','FP=' + str('%.0f' % sum([float(i[1]) for i in tracker()])),'Q','CPQ='+str('%.0f' % sum([float(i[3]) for i in tracker()])),str('%.1f' % sum([i[4] for i in tracker()])) + ' +/-',str('%.1f' % ((sum([float(i[4]) for i in tracker()])*100)/sum([float(i[1]) for i in tracker()])) )+'%'])
            self.table = Table(f, dataframe=df)
            self.table.show()
            self.update_data()
            
           
        def update_data(self):
            df = pd.DataFrame(tracker(),columns=['СС','FP=' + str('%.0f' % sum([float(i[1]) for i in tracker()])),'Q','CPQ='+str('%.0f' % sum([float(i[3]) for i in tracker()])),str('%.1f' % sum([i[4] for i in tracker()])) + ' +/-',str('%.1f' % ((sum([float(i[4]) for i in tracker()])*100)/sum([float(i[1]) for i in tracker()])) )+'%'])
            self.table.model.df = df
            self.table.redraw()
            # self.table.grid_remove()
            # self.table.grid()
            # self.pack(fill="both",expand=True)
            self.after(1000,self.update_data)
            

app = TestApp()
#launch the app
app.mainloop()