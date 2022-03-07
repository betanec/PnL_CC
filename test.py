import csv 
import pandas as pd
a = [x[1:] for x in csv.reader(open("CC_coins.csv","r"))]
print(pd.DataFrame(a).pivot(index = 0, columns=2, values=1))#.values.tolist())
# print(pd.DataFrame(a))
