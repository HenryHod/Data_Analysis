#%%
import numpy as np 
import pandas as pd
#import cpi
import matplotlib.pyplot as plt
state_gdp = pd.read_csv("state_gdp.csv")
state_tax = pd.read_csv("state_tax.csv")
income_by_state = pd.read_csv("income_by_state.csv")
state_pop = pd.read_csv("state_pop.csv")
#income_by_state = pd.read_csv("total_income_state.csv")
#state_gdp_1963 = pd.read_csv("state_gdp_1963_1997.csv").drop(["GeoFIPS","Region","TableName","Description","Unit","IndustryClassification","LineCode"],axis = 1)
#state_gdp_1997 = pd.read_csv("state_gdp_1997_2021.csv").drop(["GeoFIPS","Region","TableName","Description","IndustryClassification","Unit"],axis = 1)
#state_pop = pd.read_csv("States_Population.csv")
#state_gdp_1997 = state_gdp_1997[state_gdp_1997["LineCode"] == 1].drop(["LineCode"],axis = 1)
#state_tax = state_tax[state_tax["Name"] != "US STATE GOVTS"][["Year","State","Name","Individual Income Tax (T40)"]]
#state_tax = state_tax[state_tax["Individual Income Tax (T40)"] != "X"]
#state_tax = state_tax[state_tax["Individual Income Tax (T40)"] != "0"].reindex(axis=1)
#state_tax["Individual Income Tax (T40)"] = [float(num.replace(",","")) for num in state_tax["Individual Income Tax (T40)"]]
#income_by_state = income_by_state[income_by_state["LineCode"] == 10]
#income_by_state = income_by_state[income_by_state["GeoName"] != "United States"].drop(["GeoFIPS","TableName","Region","LineCode","Description","Unit","IndustryClassification"],axis = 1).reindex(axis = 1)
#income_by_state["GeoName"] = [(state if "*" not in state else state.replace(" *","")) for state in income_by_state["GeoName"]]
#%%
#cpi.update()
states = list(income_by_state["GeoName"])
#state_tax["GeoName"] = state_tax["State"].map(lambda x: states[x-1])
#state_pop.columns.values[:] = ["Year"]+states[:51]
#state_pop["Year"] = [year[:4] for year in state_pop["Year"]]
#for i in range(1963,1997):
#    state_gdp_1963[str(i)] = state_gdp_1963[str(i)].map(lambda x: cpi.inflate(x,i, to = 2012))
#for i in range(1963,2021):
#    income_by_state[str(i)] = income_by_state[str(i)].map(lambda x: cpi.inflate(int(float(x)),i, to = 2012))
#state_taxes_inflated = []
#for index,row in state_tax.iterrows():
#    state_taxes_inflated.append(cpi.inflate(float(row["Individual Income Tax (T40)"])/1000,row["Year"],to = 2012))
#state_tax["Individual Income Tax (T40)"] = state_taxes_inflated
#%%
#state_gdp = state_gdp_1963.merge(state_gdp_1997,on = "GeoName")
print(state_gdp)
print(state_tax)
print(income_by_state)
print(state_pop)
#state_gdp.to_csv("C:/Users/thehe/Documents/BerkBearWeb/state_gdp.csv")
#state_tax.to_csv("C:/Users/thehe/Documents/BerkBearWeb/state_tax.csv")
#income_by_state.to_csv("C:/Users/thehe/Documents/BerkBearWeb/income_by_state.csv")
#state_pop.to_csv("C:/Users/thehe/Documents/BerkBearWeb/state_pop.csv")

#%%
state_pop["Year"] = [str(year) for year in state_pop["Year"]]
all_states_dict = {state : pd.DataFrame({"Real State GDP":state_gdp.iloc[i,1:]}).reset_index(inplace=False).rename(columns = {'index':'Year'}) for i,state in enumerate(state_gdp["GeoName"])}
for i,state in enumerate(income_by_state["GeoName"]):
    all_states_dict[state] = all_states_dict[state].merge(income_by_state.iloc[i,1:].reset_index(inplace=False).rename(columns = {'index':'Year'}),on = "Year",how = "left")
    all_states_dict[state].columns.values[2] = "Real Total Income" 
state_tax["Year"] = [str(year) for year in state_tax["Year"]]
for state in states[:51]:
    all_states_dict[state] = all_states_dict[state].merge(state_tax[state_tax["GeoName"] == state].loc[:,["Year","Individual Income Tax (T40)"]],on = "Year",how = "left")
    all_states_dict[state] = all_states_dict[state].merge(state_pop.loc[:,["Year",state]], on = "Year", how = "left")
    all_states_dict[state].columns.values[3:5] = ["Real Income Tax Revenue","Population"]
    all_states_dict[state] = all_states_dict[state].iloc[1:,:]
#%%
print(all_states_dict["California"])
master_state_list = []
master_years_list = []
effective_tax_rates = []
levelized_tax_revenue = []
for state in states[:51]:
    for index,row in all_states_dict[state].iterrows():
        master_state_list.append(state)
        master_years_list.append(row["Year"])
        effective_tax_rates.append(float(row[3])/float(row[2]))
        levelized_tax_revenue.append(float(row[3])*(float(row[2])/float(row[1])))
master_df = pd.DataFrame({"Year":master_years_list,"State":master_state_list,"Effective Tax Rate":effective_tax_rates,"Levelized Tax Revenue":levelized_tax_revenue})
# %%
for state in states[:51]:
    new_master_df = master_df[master_df["State"] == state]
    plt.scatter(x = new_master_df["Effective Tax Rate"],y = new_master_df["Levelized Tax Revenue"],c = [int(year) for year in new_master_df["Year"]])
    plt.colorbar()
    plt.title(state)
    plt.show()
# %%
