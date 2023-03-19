#%%
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from custom_chart import custom
from functools import reduce
cpi = pd.read_csv('historical_cpi.csv')
ten_yr = pd.read_csv('historical_10yr.csv')
gdp = pd.read_csv('historical_gdp.csv')
unem = pd.read_csv('historical_unem.csv')
all_data = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], how='left'), [cpi,gdp,unem,ten_yr])
all_data['Date'] = [datetime.strptime(date,'%m/%d/%Y') for date in all_data.iloc[:,0]]
#%%
rec_dates = ["03/31/1879","05/31/1885","04/30/1888","05/31/1891",
"06/30/1894","06/30/1897","12/31/1900","08/31/1904","06/30/1908",
"01/31/1912","12/31/1914","03/31/1919","07/31/1921","07/31/1924",
"11/30/1927","03/31/1933","06/30/1938","10/31/1945","10/31/1949",
"05/31/1954","04/30/1958","02/28/1961","11/30/1970","03/31/1975",
"06/30/1980","11/30/1982","03/31/1991","11/30/2001","06/30/2009",
"04/30/2020"]
rec_years = [date[-4:] for date in rec_dates]
rec_dates = [datetime.strptime(date,"%m/%d/%Y") for date in rec_dates]
cpi = cpi.iloc[136:,:]
data_by_rec_dict = {year : None for year in rec_years}
date_counter = 0 
for i in range(len(rec_dates)):
    if i == len(rec_dates)-1:
        data_by_rec_dict[rec_years[i]] = all_data[all_data["Date"] >= rec_dates[i]].reindex()
    else:
        data_by_rec_dict[rec_years[i]] = all_data[(all_data["Date"] >= rec_dates[i]) & (all_data["Date"] < rec_dates[i+1])].reindex()

#%%
df_2020 = data_by_rec_dict['2020']
def chart_by_year(df,year):
    df_2020_length =  df_2020.shape[0]
    df_length = df.shape[0]
    length = df_length if df_length <= df_2020_length else df_2020_length
    fig, axs = plt.subplots(2, 2)
    plt.suptitle(year)
    df_cpi_mask = np.array(np.isfinite(df.iloc[:length,:]['CPI_Close_Percent_Change']))
    df_2020_cpi_mask = np.array(np.isfinite(df_2020.iloc[:length,:]['CPI_Close_Percent_Change']))
    axs[0, 0].plot([i for i in range(1,length+1) if df_cpi_mask[i-1]],df.iloc[:length,:]['CPI_Close_Percent_Change'][df_cpi_mask],label = year)
    axs[0, 0].plot([i for i in range(1,length+1) if df_2020_cpi_mask[i-1]],df_2020.iloc[:length,:]['CPI_Close_Percent_Change'][df_2020_cpi_mask],label = '2020')
    axs[0, 0].set_title('CPI')
    df_ten_yr_mask = np.array(np.isfinite(df.iloc[:length,:]['10yr_Close']))
    df_2020_ten_yr_mask = np.array(np.isfinite(df_2020.iloc[:length,:]['10yr_Close']))
    axs[0, 1].plot([i for i in range(1,length+1) if df_ten_yr_mask[i-1]],df.iloc[:length,:]['10yr_Close'][df_ten_yr_mask])
    axs[0, 1].plot([i for i in range(1,length+1) if df_2020_ten_yr_mask[i-1]],df_2020.iloc[:length,:]['10yr_Close'][df_2020_ten_yr_mask])
    axs[0, 1].set_title('10yr')
    df_gdp_mask = np.array(np.isfinite(df.iloc[:length,:]['GDP_Real_Percent_Change']))
    df_2020_gdp_mask = np.array(np.isfinite(df_2020.iloc[:length,:]['GDP_Real_Percent_Change']))
    axs[1, 0].plot([i for i in range(1,length+1) if df_gdp_mask[i-1]],df.iloc[:length,:]['GDP_Real_Percent_Change'][df_gdp_mask])
    axs[1, 0].plot([i for i in range(1,length+1) if df_2020_gdp_mask[i-1]],df_2020.iloc[:length,:]['GDP_Real_Percent_Change'][df_2020_gdp_mask])
    axs[1, 0].set_title('GDP')
    df_unem_mask = np.array(np.isfinite(df.iloc[:length,:]['Unem_Close']))
    df_2020_unem_mask = np.array(np.isfinite(df_2020.iloc[:length,:]['Unem_Close']))
    axs[1, 1].plot([i for i in range(1,length+1) if df_unem_mask[i-1]],df.iloc[:length,:]['Unem_Close'][df_unem_mask])
    axs[1, 1].plot([i for i in range(1,length+1) if df_2020_unem_mask[i-1]],df_2020.iloc[:length,:]['Unem_Close'][df_2020_unem_mask])
    axs[1, 1].set_title('Unemployment')
    plt.figlegend()
    plt.show()
#for year in rec_years[:-1]:
#    chart_by_year(data_by_rec_dict[year],year)

# %%
def mthly_to_qtly(data,mthly_name,qtr_name):
    new_df = pd.DataFrame(columns = ["Date",mthly_name,qtr_name])
    mthly_data = [num for num in data[mthly_name]]
    dates = [date for date in data["Date"]]
    new_qtr_data = []
    qtr_data = [num for num in data[qtr_name]]
    mth_to_qtr = 0
    new_dates = []
    for i in range(len(mthly_data)):
        if not np.isnan(qtr_data[i]):
            new_qtr_data.append(mth_to_qtr + mthly_data[i])
            new_dates.append(dates[i])
            mth_to_qtr = 0
        else:
            mth_to_qtr += mthly_data[i]
    new_df["Date"] = new_dates
    new_df[mthly_name] = new_qtr_data
    new_df[qtr_name] = [num for num in data[qtr_name] if not np.isnan(num)]
    return new_df

for i in range(all_data.shape[0]):
    if not np.isnan(all_data["GDP_Real_Percent_Change"][i]):
        gdp_start = i
        break
print(gdp_start)
cpi_gdp = mthly_to_qtly(all_data.iloc[gdp_start:,:],"CPI_Close_Percent_Change","GDP_Real_Percent_Change")
print(cpi_gdp)
plt.scatter(cpi_gdp["CPI_Close_Percent_Change"],cpi_gdp["GDP_Real_Percent_Change"], c = cpi_gdp["Date"],cmap = "cividis")
plt.show()

# %%
