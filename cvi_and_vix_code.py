# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from custom_chart import custom
from datetime import datetime
#%%
cvi_and_vix = pd.read_csv("cvi_and_vix.csv")
# %%
cvi_data = cvi_and_vix.iloc[2:,:2].reindex().dropna()
vix_data = cvi_and_vix.iloc[2:,2:].reindex().dropna()
cvi_data.iloc[:,0] = [datetime.strptime(date,"%m/%d/%Y")for date in cvi_data.iloc[:,0]]
vix_data.iloc[:,0] = [datetime.strptime(date,"%m/%d/%Y") for date in vix_data.iloc[:,0]]
cvi_date_list = list(cvi_data.iloc[:,0])
print(len(cvi_date_list))
cvi_change = list(cvi_data.iloc[:,1])
print(len(cvi_change))
vix_date_list = list(vix_data.iloc[:,0])
print(len(vix_date_list))
vix_change = list(vix_data.iloc[:,1])
print(len(vix_change))
fig = plt.figure(figsize = (7,5.5))
custom = custom(fig)
custom.chart_type = custom.ax1.plot_date(cvi_date_list,cvi_change)
#custom.ax2.plot()
plt.xlim()
custom.chart_maker()
plt.show()
