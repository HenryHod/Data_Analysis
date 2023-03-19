import pandas as pd
import yfinance as yf
from datetime import datetime
sp_data = yf.download('^GSPC')
sp_data = pd.DataFrame(sp_data)
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
ten_day_percentage = int((ten_list/all_time_high_count)*100)
five_day_percentage = int((five_list/all_time_high_count)*100)
one_day_percentage = int((one_list/all_time_high_count)*100)
print(ten_day_percentage)
print(five_day_percentage)
print(one_day_percentage)
ytd_highs_count = 0
ytd_days = (datetime(2022,1,1) - datetime.now()).days
last_year_highest_price = sp_data['Close'][ytd_days]
for x in reversed(range(1,ytd_days-1)):
    if  sp_data['Close'][-x] > last_year_highest_price:
        last_year_highest_price = sp_data['Close'][-x]
        ytd_highs_count += 1
print(ytd_highs_count)
