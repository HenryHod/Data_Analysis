#%%
import matplotlib.pyplot as plt
from datetime import date, datetime
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import nasdaqdatalink as nasdaq
from fredapi import Fred
fred = Fred(api_key="179a8a574defbe5d2bb69cc07b59beb2")
#%%
historical_cpi = pd.read_csv("cpi.csv",na_values=[""])
sp_sectors_df = pd.read_csv("sp_sectors.csv",na_values=[""])
historical_cpi["Date"] = [datetime.strptime(date, "%m/%d/%Y") for date in historical_cpi["Date"].values]
sp_sectors_df["Date"] = [datetime.strptime(date, "%m/%d/%Y") for date in sp_sectors_df["Date"].values]
#%%
value = fred.get_series("WILLLRGCAPVAL").dropna().to_frame().rename_axis("Date").rename({0:"Index"}, axis = 1)
growth = fred.get_series("WILLLRGCAPGR").dropna().to_frame().rename_axis("Date").rename({0:"Index"},axis = 1)
value["%Change"] = [0] + value["Index"].pct_change().values
growth["%Change"] = [0] + growth["Index"].pct_change().values
dates = value.rename_axis("Date").reset_index()["Date"].values
wil5000 = fred.get_series("WILLLRGCAP").dropna().to_frame().rename_axis("Date").rename({0:"Close"}, axis = 1)
cpi = fred.get_series("CPIAUCSL").dropna().to_frame().rename_axis("Date").rename({0:"Value"}, axis = 1).reset_index()
recessions = fred.get_series("USREC").dropna().to_frame().rename_axis("Date").rename({0:"Value"}, axis = 1).reset_index()
g_v_difference = pd.DataFrame({"Date":dates,"G_V_Difference":growth["Index"].values /value["Index"].values,"Growth": growth["Index"].values,"Value": value["Index"].values})
#%%
last_date = pd.Timestamp(dates[len(dates)-1])
merged_df = g_v_difference.merge(wil5000,how = "left",on = "Date")
recessions_daily = []
recession_returns = []
for i in range(1,len(recessions["Date"].values)):
    df = merged_df[(recessions["Date"].values[i-1] <= merged_df["Date"]) & (merged_df["Date"] < recessions["Date"].values[i])]
    [recession_returns.append(recessions["Value"].values[i-1]) for i in range(df.shape[0])]
    recessions_daily = recessions_daily + df["Date"].tolist()
recessions_daily_df = pd.DataFrame({"Date": recessions_daily,"Recession": recession_returns})
merged_df["Year"] = pd.DatetimeIndex(merged_df["Date"]).year
merged_df = recessions_daily_df.merge(merged_df, on  = "Date", how = "left")
#merged_df = merged_df[merged_df["Recession"] == 0.0].reset_index()
merged_df[["WIL5000 %Change","Growth_%Change","Value_%Change"]] = merged_df[["Close","Growth","Value"]].pct_change()
merged_df["G_V_%Change"] = merged_df["Growth_%Change"].values - merged_df["Value_%Change"].values
merged_df = merged_df.iloc[1:,:]
#sp500_change = [(merged_df["Close"][x-1]-merged_df["Close"][x])/merged_df["Close"][x-1] for x in range(1,merged_df.shape[0])]
#g_v_change = [(merged_df["G_V_Difference"][x-1]-merged_df["G_V_Difference"][x])/merged_df["G_V_Difference"][x-1] for x in range(1,merged_df.shape[0])]
period_percent_changes = []
rolling_correlation = []
correlation_dates = []
print(merged_df)
merged_df = merged_df.iloc[1:,:]
#%%
#returns_scatter_fig = go.Figure()
#returns_scatter_fig.add_trace(go.Scatter(merged_df, x = "Value_%Change", y = "Growth_%Change", color_continuous_scale="cividis", color = merged_df["Year"]))
#returns_scatter_fig.update_layout(title = dict(text = "<b>Growth vs. Value Returns Since 1980</b>", x = 0.5), font = dict(family = "Georgia"), 
#                                yaxis_title_text = "Value Daily Returns",xaxis_title_text = "Growth Daily Returns", margin = dict(t = 20))
#
#returns_scatter_fig.write_html("Research+Publications/Market+Foresight/returns_scatter.html")
hist_source = f"Source: CC Capital, FRED; Data as of {last_date.month}-{last_date.day}-{last_date.year}"
returns_hist_fig = go.Figure()
returns_hist_fig.add_trace(go.Histogram(x = merged_df["Growth_%Change"].values * 100, histnorm="probability density", marker_color = "blue", name = "Growth", hovertemplate="Range: %{x}<br>Percent: %{y:.2f}<extra></extra>"))
returns_hist_fig.add_trace(go.Histogram(x = merged_df["Value_%Change"].values * 100, histnorm = "probability density", marker_color = "gold", name = "Value", hovertemplate="Range: %{x}<br>Percent: %{y:.2f}<extra></extra>"))
returns_hist_fig.update_layout(font = dict(family = "Georgia"),title = dict(text = "<b>Growth and Value Returns</b>", x = 0.5),
barmode = "overlay",legend=dict(y=1.1,x = 0.3, orientation='h', font = dict(size = 10)), yaxis_title_text = "Probability Density",
xaxis_title_text = f"Daily Return (%)<br><sup>{hist_source}</sup>", title_font_size = 20)
returns_hist_fig.update_traces(opacity = 0.5)
returns_hist_fig.update_xaxes(range = [-4,4], title_standoff = 10)
returns_hist_fig.update_yaxes(title_standoff = 10)
returns_hist_fig.write_html("Research+Publications/Market+Foresight/returns_histogram.html")
#%%
blue_colors = n_colors("rgb(0,60,130)","rgb(175,215,255)",3,"rgb")
#gold_colors = n_colors()
growth_value_groups = {"Sector":["Agriculture","Goods and Services","Digital Information",
 "Energy", "Financials","Health Care","Industrials","Real Estate", "Materials","Technology",
 "Transportation","Agriculture","Goods and Services","Digital Information",
 "Energy", "Financials","Health Care","Industrials","Real Estate", "Materials","Technology",
 "Transportation","Agriculture","Goods and Services","Digital Information",
 "Energy", "Financials","Health Care","Industrials","Real Estate", "Materials","Technology",
 "Transportation"],"Percent":[6.29,9.95, 9.36,12.43,22.36,12.48,7.03,2.34,3.80, 10.52,3.44,0.93,13.69,32.62,
  1.38, 9.13, 12.40, 2.59, 3.61, 1.45, 17.08, 5.11,3.73,11.74,20.49,7.15,16.03,12.44,4.91,2.95,2.68,13.66,
  4.24],"Group": ["Value" for i in range(11)]+["Growth" for i in range(11)]+["All" for i in range(11)]}
g_v_sectors_df = pd.DataFrame(growth_value_groups)
#print(g_v_sectors_df.pivot(columns ="Sector"))
bar_fig = px.bar(g_v_sectors_df,x = "Sector",y = "Percent",color = "Group",barmode = "group", color_discrete_sequence=blue_colors)
bar_fig.update_layout(legend_title_text = None, font = dict(family = "Georgia"),title = dict(text = "<b>Growth and Value Sector Weights</b>", x = 0.5),
                    title_font_size = 20,xaxis_title = f"<sup>Source: CC Capital; Data as of 9-26-2022</sup>",
                    legend=dict(y=1.1,x = 0.3, orientation='h', font = dict(size = 10)),
                    margin = dict(t = 60, r = 10,l = 10,b = 0))
bar_fig.update_xaxes(tickfont_size = 10, tickangle = 45)
bar_fig.write_html("Research+Publications/Market+Foresight/sector_bars.html")
#%%
for i in range(59,merged_df.shape[0],60):
    rolling_correlation.append(np.corrcoef(merged_df["WIL5000 %Change"][i-60:i+1].values,merged_df["G_V_%Change"][i-60:i+1].values)[0][1])
    correlation_dates.append(merged_df["Date"][i].year)
    period_percent_changes.append(sum(merged_df["WIL5000 %Change"][i-60:i+1].values))
cpi = cpi[cpi["Date"] >= dates[0]]
cpi_dates = cpi["Date"].values
g_v_difference_one_month = []
historical_cpi_dates = historical_cpi["Date"].values
new_sp_sectors_df = pd.DataFrame(columns=sp_sectors_df.columns[1:])
cpi_dates_counted = []
for i in range(1,len(historical_cpi_dates)):
    df = sp_sectors_df[(sp_sectors_df["Date"] > historical_cpi_dates[i-1]) & (sp_sectors_df["Date"] <= historical_cpi_dates[i])]
    df_dates = df["Date"].values
    if len(df_dates) > 0:
        cpi_dates_counted.append(df_dates[-1])
        df_sums = df.iloc[:,1:].sum(min_count = 1).to_frame().T
        new_sp_sectors_df = new_sp_sectors_df.merge(df_sums,how = "outer")
new_sp_sectors_df = new_sp_sectors_df.set_axis(cpi_dates_counted).rename_axis("Date").reset_index()
#%%
#print(len(rolling_correlation))
#print(len(correlation_dates))
#plt.plot(correlation_dates,rolling_correlation)
#plt.show()
#%%
#line_fig1 = go.Figure()
#line_fig1.add_trace(go.Scatter(x = merged_df["Date"],y = merged_df["Growth_%Change"]-merged_df["Value_%Change"]))
#line_fig1.add_trace(go.Scatter(x = merged_df["Date"],y = merged_df["Recession"],fill = "tozeroy"), secondary_y = True)
#line_fig1.update_layout(
#    margin=go.layout.Margin(
#        t = 5,
#        l=5, #left margin
#        r=5, #right margin
#        b=5, #bottom margin
#    ),
#    title_x = 0.5,
#    title_font_size = 25,
#    font_family = "Georgia",
#    title_font_family = "Baskerville",
#    title_font_color = "black"
#)
#line_fig1.write_html("Research+Publications/Market+Foresight/g_v_difference_line.html")
#%%
#print(type(dates[0]))
#%%
r = merged_df[["Growth_%Change","Value_%Change"]].corr()["Growth_%Change"][1]
mean_x = np.mean(merged_df["Growth_%Change"])
mean_y = np.mean(merged_df["Value_%Change"])
std_x = np.std(merged_df["Growth_%Change"])
std_y = np.std(merged_df["Value_%Change"])
print((std_x-std_y)/std_y)
b = (r*std_y)/std_x
a = mean_y-b*mean_x
residuals = merged_df["Value_%Change"].values - (a + b*merged_df["Growth_%Change"].values)
#plt.scatter(merged_df["Growth_%Change"], residuals)
#plt.xlim(-0.10,0.10)
#plt.show()
#plt.hist(residuals, bins=50)
#print(a,b)
#%%
#x = np.linspace(-0.2,0.1,100)
#print(merged_df)
#print(np.corrcoef(merged_df["Value_%Change"],merged_df["Growth_%Change"]))
figure_1_source = f"Source: Standard & Poor, FTSE Russell, Yahoo Finance, Nasdaq Data Link; Data as of {last_date.month}-{last_date.day}-{last_date.year}"
scatter_fig1 = go.Figure()
scatter_fig1.add_trace(go.Scatter(x = merged_df["Growth_%Change"].values*100, mode = "markers",y = merged_df["Value_%Change"].values * 100, text = merged_df["Year"],marker = dict(color = merged_df["Year"],
colorscale="cividis", colorbar = dict(thickness = 10)),
    opacity=0.75, hovertemplate='<br>Growth: %{x:.2f}%<br>Value: %{y:.2f}%<br>Year: %{text}<extra></extra>'))
scatter_fig1.update_layout(
    margin=go.layout.Margin(
        l=20, #left margin
        r=20, #right margin
        b=0, #bottom margin
        t=60
    ),
    title="<b>Growth vs Value</b>",
    yaxis = go.layout.YAxis(
        title = go.layout.yaxis.Title(
            standoff = 10
        )
    ),
    xaxis = go.layout.XAxis(
        title=go.layout.xaxis.Title(
            standoff = 10,
            text=f"Growth Daily Returns<br><sup>{figure_1_source}</sup>"
            )
        ),
    yaxis_title = "Value Daily Returns",
    title_x = 0.5,
    title_font_size = 25,
    font_family = "Georgia",
    title_font_family = "Baskerville",
)
scatter_fig1.write_html("Research+Publications/Market+Foresight/returns_scatter.html",full_html = False,include_plotlyjs = 'cdn')
#px.scatter(merged_df,"Close","G_V_Difference",color = merged_df["Year"],facet_col=merged_df)
# %%
sp_sectors = new_sp_sectors_df.columns[1:11]
corrs_dict = {ticker:{"Highest Corr":0,"Months Apart":0} for ticker in sp_sectors}
for i in range(6):
    corrs_df = new_sp_sectors_df.iloc[i:,:].merge(historical_cpi.iloc[:-i,:]).corr()
    corrs = corrs_df["Close_Percent_Change"].values[:10]
    for a,corr in enumerate(corrs):
        if abs(corr) > abs(corrs_dict[sp_sectors[a]]["Highest Corr"]):
            corrs_dict[sp_sectors[a]]["Highest Corr"] = corr
            corrs_dict[sp_sectors[a]]["Months Apart"] = i
# %%
merged_sp_sectors = new_sp_sectors_df.iloc[1:,:].merge(historical_cpi.iloc[:-1,:]) 
merged_sp_sectors = merged_sp_sectors.merge(merged_df[["Date","Growth_%Change","Value_%Change"]])
deflationary = merged_sp_sectors[merged_sp_sectors["Close_Percent_Change"] < 0]
zero_to_five = merged_sp_sectors[(merged_sp_sectors["Close_Percent_Change"] >= 0) & (merged_sp_sectors["Close_Percent_Change"] < 0.05/12.0)]
five_to_ten = merged_sp_sectors[(merged_sp_sectors["Close_Percent_Change"] >= 0.05/12.0) & (merged_sp_sectors["Close_Percent_Change"] < 0.1/12.0)]
greater_than_ten = merged_sp_sectors[merged_sp_sectors["Close_Percent_Change"] >= 0.1/12.0]
def cpi_grouper(cpi):
    if cpi < 0:
        return "CPI < 0%"
    elif 0 <= cpi < 0.05/12:
        return  "0% <= CPI > 5%"
    elif 0.05/12 <= cpi < 0.1/12:
        return "5% <= CPI > 10%"
    else:
        return "CPI >= 10%"
all_returns = merged_sp_sectors.reset_index().drop("index", axis = 1).mean().to_frame().transpose()
all_returns["CPI Group"] = ["All"]
merged_sp_sectors["CPI Group"] = merged_sp_sectors["Close_Percent_Change"].apply(lambda x: cpi_grouper(x))
median_returns_df = merged_sp_sectors.groupby(["CPI Group"]).mean().reset_index()
print(all_returns)
median_returns_df = median_returns_df.merge(all_returns, how = "outer").set_index("CPI Group")
print(median_returns_df)
median_returns_df = median_returns_df.apply(lambda x: np.round(x*12*100,2))#.reindex({"CPI Group":["CPI < 0%","0% <= CPI > 5%","5% <= CPI > 10%","CPI >= 10%"]})
median_returns_df = median_returns_df.reset_index().reindex([4,2,0,1,3]).reset_index().drop(axis = 1,labels = ["index"])
median_returns_df = median_returns_df.rename(columns = {"CPI Group":"Ann. Inflation","SP10":"Energy","SP15":"Materials"
                        ,"SP20":"Industrials","SP25":"Consumer Discretionary","SP30":"Consumer Staples",
                        "SP35":"Health Care","SP40":"Financial","SP45":"Information Technology","SP50":"Comm.",
                        "SP55":"Utilities","Close_Percent_Change":"CPI","Growth_%Change": "Growth","Value_%Change": "Value"})
#returns_df = pd.DataFrame({"Inflation":["CPI < 0%","0% <= CPI > 5%","5% <= CPI > 10%"," CPI >= 10%"],
                           # "Energy":empty_list,"Materials":empty_list,"Industrials":empty_list,"Consumer Discretionary":empty_list,
                            #"Consumer Staples":empty_list,"Health Care":[],"Financials":[],"Information Technology":[],
                            #"Communications":[],"Utilities":[]})
#deflationary_medians = deflationary.median(axis =1)
#for sector in returns_df.columns[1:]:
#    returns_df.loc[sector:0] = deflationary_medians[sector].values
#print(returns_df)
# %%

red_colors = np.array(n_colors('rgb(255, 200, 200)', 'rgb(100, 0, 0)', 6, colortype='rgb'))
green_colors = np.array(n_colors('rgb(200, 255, 200)', 'rgb(0, 100, 0)', 6, colortype='rgb'))
values_list = [median_returns_df[column].values.tolist() for column in median_returns_df.columns]
def color_switcher(value):
    value = float(value)
    if value >= 0:
        return green_colors
    else:
        return red_colors
def light_to_dark(value):
    val = abs(float(value))
    if val < 5:
        return 0
    elif val < 10:
        return 1
    elif val < 25:
        return 2
    elif val < 40:
        return 3
    else: 
        return 4
def text_color(cell_color_index):
    if cell_color_index > 1:
        return "rgb(255,255,255)"
    else:
        return "rgb(60,60,60)"
#%%
#print(values_list)
#one_color = color_switcher(values_list[1][1:2])
#print([[color_switcher(column)[index-1] for index in light_to_dark(column)] for column in values_list[1:]])
fill_color=[["rgb(255.0,255.0,255.0)" for i in range(4)]]+[ [color_switcher(column[i])[light_to_dark(column[i])] for i in range(len(column))] for column in values_list[1:]]
font_color = [["rgb(100,100,100)" for i in range(4)]]+[[text_color(color_index) for color_index in color_index_list] for color_index_list in [[light_to_dark(column[i]) for i in range(len(column))] for column in values_list[1:]]]
#%%
table_fig = go.Figure(data=[go.Table(
    columnwidth = [22]+[9,10,10,14,10,10,10,12,9,9,6,9,9],
    header = dict(values = median_returns_df.columns,
                line_color="rgb(150,150,150)",font_size = 12),
    cells=dict(
        values=[median_returns_df[column].values.tolist() for column in median_returns_df.columns],
        line_color="rgb(150,150,150)",
        fill_color=fill_color,
        font = dict(color = font_color, size = 10),
        align = ["center","center"],
        height = 40,
    ))
])
table_fig.update_layout(
        font_family = "Georgia",
        height = 268,
        width = 975,
        margin=dict(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t = 0,
    ),
    annotations=[
        go.layout.Annotation(
            showarrow=False,
            text=f'Source: Standard & Poor, FRED, CC Capital; Data as of {last_date.month}-{last_date.day}-{last_date.year}',
            x=0.5,
            yanchor='bottom',
            y=0
        )],
    autosize = False)

table_fig.write_html("Research+Publications/Market+Foresight/sector_returns_table.html",full_html = True)
# %%
