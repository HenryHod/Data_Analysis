# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from custom_chart import custom
from datetime import datetime
# %%
crypto_data = pd.read_csv('raw_crypto_data.csv',low_memory = False)
# %%
def coin_finder(string):
    if pd.isna(string) != True and "-" in string:
        return string.split("-")[0]
    return string

crypto_data["Chain"] = crypto_data["Chain"].apply(coin_finder)
# %%
#print(crypto_data.head())
crypto_data_by_coin = crypto_data.iloc[:,2:]
crypto_data_by_coin.iloc[0,0] = "Date"
crypto_data_by_coin.iloc[1,0] = "Total"
crypto_data_by_coin = crypto_data_by_coin.drop(crypto_data_by_coin.columns[1], axis = 1)
crypto_data_by_coin.iloc[2:,1:] = crypto_data_by_coin.iloc[2:,1:].astype(float)
crypto_data_by_coin = crypto_data_by_coin.groupby("Chain",as_index = False).sum()
crypto_data_by_coin = crypto_data_by_coin.drop(index = 4)
coin_list = [coin for coin in crypto_data_by_coin.iloc[:,0] if coin != "Date" or coin != "Total"]
#%%
crypto_data_by_category = crypto_data.drop(crypto_data.columns[3],axis = 1)
crypto_data_by_category = crypto_data_by_category.drop("Chain",axis = 1)
crypto_data_by_category = crypto_data_by_category.drop(index = 1)
# %%
crypto_data_by_category.iloc[1:,2:] = crypto_data_by_category.iloc[1:,2:].astype(float)
crypto_data_by_category.iloc[1:,2:] = crypto_data_by_category.iloc[1:,2:].fillna(0)
crypto_data_by_category = crypto_data_by_category.iloc[:,1:]
crypto_data_by_category.iloc[0,0] = "Date"
crypto_data_by_category= crypto_data_by_category.groupby("Category",as_index = False,sort = False).sum()
# %%
crypto_data_by_category.iloc[1:,:] = crypto_data_by_category.iloc[1:,:].sort_values(
    crypto_data_by_category.iloc[1:,:].columns[1213],ascending=False).reindex()
#crypto_data_by_category =  crypto_data_by_category.transpose()
crypto_cleaned_cat = pd.DataFrame()
crypto_cleaned_cat["Date"] = [i for i in crypto_data_by_category.iloc[0,1:]]
# %%
crypto_data_by_coin.iloc[1:,:] = crypto_data_by_coin.iloc[1:,:].sort_values(crypto_data_by_coin.iloc[1:,:].columns[1213],ascending=False)
crypto_data_by_coin = crypto_data_by_coin.drop(index = [3,6],axis = 0).reindex()
date_list = [item for item in crypto_data_by_coin.iloc[0,:]][1:]
crypto_cleaned = pd.DataFrame({"Date":date_list})
#print(crypto_data_by_coin.head(12))
#%%
def total_row_maker(table):
    total_list = []
    for i in range(1213):
        total_list.append(sum([(float(item) if not isinstance(item,str) else 0 )for item in table.iloc[:,i]]))
    return total_list
crypto_cleaned_cat["Total"] = total_row_maker(crypto_data_by_category.iloc[1:,1:])
crypto_cleaned["Total"] = total_row_maker(crypto_data_by_coin.iloc[1:,1:])
for i in [1,2,5,7,8]:
    crypto_cleaned[crypto_data_by_coin["Chain"][i]] = list(crypto_data_by_coin.iloc[i,1:])
crypto_cleaned["Other"] = total_row_maker(crypto_data_by_coin.iloc[9:30,1:])
crypto_cleaned.iloc[1:,1:] = crypto_cleaned.iloc[1:,1:].astype(float)
#print(crypto_cleaned)
# %%
#print(crypto_data_by_category.head())
for k in range(1,6):
    crypto_cleaned_cat[crypto_data_by_category["Category"][k]] = list(crypto_data_by_category.iloc[k,1:])

crypto_cleaned_cat["Other"] = total_row_maker(crypto_data_by_category.iloc[8:26,1:])

data_lst = []
for i in range(6):
    data_lst.append(list(crypto_cleaned_cat.iloc[600:,i+2]))

fig1 = plt.figure()
custom = custom(fig1)
colors_list = [custom.colors[key] for key in custom.colors]
custom.chart_type = custom.ax1.stackplot(date_list[600:],data_lst[0],data_lst[1],data_lst[2],data_lst[3],data_lst[4],data_lst[5],
labels = ["Lending","DeFi Exchanges","Yield","Bridge","Staking","Other"],colors = colors_list
)
custom.title = "Total Value Locked By Category"
custom.ylabel = "Locked Value (Hundred Billions)"
custom.x_ticks = range(0,len(date_list[600:]),100)
date_labels = [date_list[600 +i][-7:] for i in range(0,len(date_list[600:]),100)]
custom.x_ticklabels = [ date[1:] if date[0] == "0" or date[0] == "/" else date for date in date_labels]
custom.legend = True
custom.chart_maker()
plt.xlim(0,613)
plt.show()

#%%
data_list = []
for i in range(6):
    data_list.append(list(crypto_cleaned.iloc[600:,i+2]))
#print(crypto_cleaned)
fig2 = plt.figure()
custom = custom(fig2)
colors_list = [custom.colors[key] for key in custom.colors]
custom.chart_type = custom.ax1.stackplot(date_list[600:],data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],labels = ["Ethereum","Terra","Fantom","Bitcoin","Avalanche","Other"],colors = colors_list
)

# %%
custom.title = "Total Value Locked By Chain"
custom.ylabel = "Locked Value (Hundred Billions)"
custom.x_ticks = range(0,len(date_list[600:]),100)
date_labels = [date_list[600 +i][-7:] for i in range(0,len(date_list[600:]),100)]
custom.x_ticklabels = [ date[1:] if date[0] == "0" or date[0] == "/" else date for date in date_labels]
custom.legend = True
custom.chart_maker()
plt.xlim(0,613)
plt.show()