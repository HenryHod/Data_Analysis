import pandas as pd
from matplotlib import pyplot as plt
import yfinance as yf
from datetime import datetime
import numpy as np
sp_data = yf.download('^GSPC')
sp_data = pd.DataFrame(sp_data)
#print(sp_data.head())
highest_price = 0
all_time_high_count = 0
day_count = 0
day_count_list = []
for price in sp_data['Close']:
    if price > highest_price:
        highest_price = price
        all_time_high_count += 1
        day_count_list.append(day_count)
        day_count =0 
    elif price <= highest_price:
        day_count += 1
print(all_time_high_count)
ten_list = 0
five_list = 0
one_list = 0 
for day_count in day_count_list:
    if day_count <=10:
        ten_list += 1
        if day_count <= 5:
            five_list += 1
            if day_count <= 1:
                one_list += 1
ten_day_percentage = ten_list/all_time_high_count
five_day_percentage = five_list/all_time_high_count
one_day_percentage = one_list/all_time_high_count
print(ten_day_percentage)
print(five_day_percentage)
print(one_day_percentage)
last_year_highs_count = 0
number_of_trading_days_2021 = 287
last_year_highest_price = sp_data['Close'][-number_of_trading_days_2021]
for x in reversed(range(1,number_of_trading_days_2021-1)):
    if  sp_data['Close'][-x] > last_year_highest_price:
        last_year_highest_price = sp_data['Close'][-x]
        last_year_highs_count += 1
print(last_year_highs_count)
