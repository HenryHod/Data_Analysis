#%%
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from custom_chart import custom

#%%
russell_data = pd.read_csv('russell_2000_data.csv', encoding = 'unicode_escape')
russell_data = russell_data.iloc[:,:6]
# %%
russell_data_na_free = russell_data[russell_data['5Y %Chg'].isna() != True]
russell_data_na_free = russell_data_na_free[russell_data['Beta'].isna() != True]
russell_data_na_free = russell_data_na_free[russell_data['Sector'].isna() != True]
russell_data_na_free = russell_data_na_free.reindex()
def total_percent_to_ann_return(percentage):
    if '%' in percentage:
        return float(percentage.strip('%'))/5
    else:
        return float(percentage)/5
sector_list = sorted(russell_data_na_free['Sector'].unique())

russell_data_na_free['5Y %Chg'] = russell_data_na_free['5Y %Chg'].apply(total_percent_to_ann_return)
russell_data_by_sector = russell_data_na_free['Beta'].groupby(russell_data_na_free['Sector']).mean()
russell_data_by_sector = pd.merge(russell_data_by_sector,russell_data_na_free['5Y %Chg'].groupby(russell_data_na_free['Sector']).mean(), on = 'Sector')
russell_data_by_sector = pd.merge(russell_data_by_sector,russell_data_na_free['5Y %Chg'].groupby(russell_data_na_free['Sector']).count(), on = 'Sector')


#print(russell_data_by_sector.head())
#russell_data_na_free['Beta'] = russell_data_na_free['Beta'].apply(lambda x: x*100)

# %%
fig = plt.figure(figsize = (7,5.5))
custom = custom(fig)
custom.chart_type = custom.ax.scatter(russell_data_by_sector['5Y %Chg_x'],
russell_data_by_sector['Beta'],s = np.array(russell_data_by_sector['5Y %Chg_y'])*12.5,c = cm.cividis(range(0,320,20)),alpha = 0.60)
custom.xlabel = '5 Year Annual Returns'
custom.ylabel = '60 Month Rolling Beta'
custom.title = "Russell 2000 Constituents\nAnnual Returns and Beta by Sector"
custom.x_ticks = range(4,21,2)
custom.x_ticklabels = [str(i) + '%' for i in range(4,21,2)]
custom.chart_maker()
label_dict = {}
for i,sector in enumerate(sector_list):
    label_dict[sector] = [russell_data_by_sector['5Y %Chg_x'][i],russell_data_by_sector['Beta'][i]]
label_dict['Transportation'][1] -= .015 
label_dict['Consumer Discretionary'][0] -= 1
label_dict['Medical'][1] += .020
label_dict['Industrial Products'][0] -= 0.25
for sector in label_dict:
    plt.text(label_dict[sector][0] -1 ,label_dict[sector][1],sector,**custom.font,fontsize = 8)
plt.xlim(2.5,20)
plt.ylim(0.5,2.5)
plt.show()

# %%
