import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
tax_stats = pd.read_csv("real_tax_stats.csv")
real_gdp_per_capita = pd.read_csv("gdp_per_capita.csv")
population = pd.read_csv("population.csv")
new_real_gdp_per_capita = []
years = []
real_gdp = []
for i,gdp in enumerate(real_gdp_per_capita["Per_Capita"]):
    if real_gdp_per_capita["Date"][i][:2] == "12":
        new_real_gdp_per_capita.append(gdp)
        real_gdp.append(real_gdp_per_capita["Close"][i])
        years.append(real_gdp_per_capita["Date"][i][-4:])
gdp_per_capita_df = pd.DataFrame({"Year":years,"Real GDP":real_gdp,"Real_GDP_Per_Capita":new_real_gdp_per_capita})
gdp_per_capita_df["Year"] = [int(year) for year in gdp_per_capita_df["Year"]]
merged_df = tax_stats.merge(gdp_per_capita_df,how = "left",on = "Year")
decades = [str(year)[:3]+"0" for year in merged_df["Year"]]
merged_df["Decade"] = decades
merged_df["Real Total Income"] = merged_df["Real Total Income"]* 1.1756
merged_df["Real Tax Revenue"] = merged_df["Real Tax Revenue"]* 1.1756
tax_rates = merged_df["Real Tax Revenue"]/merged_df["Real Total Income"]
merged_df["Population"] = population["Close"]
merged_df["Average Income Per Capita"] = merged_df["Real Total Income"]/merged_df["No. of Returns"]
merged_df["Percent of Pop Paying Taxes"] = merged_df["No. of Returns"]/merged_df["Population"]
merged_df["Effective_Tax_Rate"] = tax_rates
merged_df["Idealized Tax Revenue"] = (tax_rates*merged_df["Average Income Per Capita"])*merged_df["Population"]
merged_df["Levelized Tax Revenue Gap"] = (merged_df["Idealized Tax Revenue"]-merged_df["Real Tax Revenue"])/merged_df["Real GDP"]
#fig,ax1 = plt.subplots()
#ax2 = ax1.twinx()
#ax1.plot(merged_df["Year"],merged_df["Effective_Tax_Rate"])
#ax2.plot(merged_df["Year"],merged_df["Levelized Tax Revenue Per Taxpayer"])
plt.scatter(merged_df["Effective_Tax_Rate"],merged_df["Levelized Tax Revenue Gap"],c = merged_df["Year"])
plt.colorbar()
plt.show()