import dash
from dash import Dash, dcc, html, Input, Output,ALL
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.subplots
import yfinance as yf
import pandas as pd
import numpy as np
colors = {'golden_rod' : '#CC9900','berkeley_blue' : '#00203e','yellow_gold' : '#FFCC00',
        'sky_blue': '#548DD4','navy_blue': '#386295','midnight_blue': '#17365D'}
colors = list(colors.values())
ticker_dict = {"S&P 500":"^GSPC","VIX":"^VIX","Dow Jones":"^DJI"}
full_ticker_list = list(ticker_dict.keys())
app = Dash(__name__,external_scripts=["berkbear.css"],suppress_callback_exceptions=True)
app.layout = html.Div([
    html.Div([dcc.Dropdown(
        id="dropdown",
        options=full_ticker_list,
        clearable=True,
        multi = True
    )
    ], id = "choices"),
    html.Div(
        [html.Div(
            [html.Div(id = "ticker_preferences",className="menu"),
            html.A(href="#ticker_preferences", id = "ticker_preferences_icon"),
            dcc.Loading([dcc.Graph(id="graph",config= {'displaylogo': False})],type = "graph")],id = "figure")])
    ],id = "master")
@app.callback(
    Output("ticker_preferences","children"),
    Output("ticker_preferences_icon","children"),
    Input("dropdown","value"))
def div_maker(tickers):
    div_list = []
    link  = []
    if tickers is not None:
        if type(tickers) == str:
            tickers = [tickers]
        if len(tickers) > 0:
            div_list = [html.A(href="#",id="close")]
            link = [html.Img(src = "/assets/hamburger.png",id = "hamburger")]
        for i,ticker in enumerate(tickers):
            div_list.append(html.Div([
            html.H3(ticker,id="ticker_title"),

            html.Div([
                html.Div([html.Div([
                        dcc.DatePickerRange(className="date_range_picker",id = {"type":"date_picker","index":i},min_date_allowed=datetime.strptime("1970-01-01","%Y-%m-%d")),
                        html.A(children = [html.Img(src = "/assets/calendar.png",className="calendar_png")])]
                        ,id = "calendar_div"+str(i),className="date_picker_div")]+
                        [(html.Button(period,id = {"type":"period_btn","index":a*(i+1)},className="period_button") if period != "max" else html.Button(period,id = {"type":"period_btn","index":a},className="period_button",autoFocus=True,n_clicks = 1))
                        for a,period in enumerate(["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"])
                        ], id = {"type":"period_select","index":i},className = "period_buttons_container"),

                html.Div([

                    html.Div([
                        html.H6("Interval:",className = "interval_title"),
                        dcc.Dropdown(id = {"type":"interval_select","index":i},options = ["1m","2m","5m","15m","30m","60m","90m","1d","5d","1wk","1mo","3mo"],value = "1d",clearable=False,searchable=False,className="interval_select")
                    ], className="option"),

                    html.Div([
                        html.H6("Line Type:",className = "line_title"),
                        dcc.Dropdown(clearable=False,searchable=False,className="line_select",id = {"type":"line_type","index":i},
                options=["Linear","Area","Candle"],value = "Linear")
                    ],className = "option"),

                    html.Div([
                        html.H6("Transform:",className = "transform_title"),
                        dcc.Dropdown(searchable=False,clearable = False,id =  {"type":"transform","index":i},className = "transform_select",
                        options = ["Level","Natural Log","Change","%Change","Cumulative","%Cumulative"],value = "Level")
                    ],className = "option"),

                    html.Div([
                        (dcc.Checklist(id =  {"type":"axis","index":i},className = "axis_select",labelStyle=dict(display="block"),
                        options = ["Secondary Y-axis","Secondary X-axis"],value = ["None"],style = {"padding": "0px 10px"}) if len(tickers) > 1 else dcc.Checklist())],className = "option"
                    )], className="options_list")])],className="ticker_menu",id = {"type":"ticker","index":i},title = str(i)))
    return div_list,link
@app.callback(Output({"type":"interval_select","index":ALL},"value"),
              Output({"type":"interval_select","index":ALL},"options"),
              Output({"type":"date_picker","index":ALL},"start_date"),
              Output({"type":"date_picker","index":ALL},"end_date"),
              Input("dropdown","value"),
              Input({"type":"period_btn","index":ALL},"n_clicks"),
              Input( {"type":"period_btn","index":ALL},"children"),
              Input({"type":"date_picker","index":ALL},"start_date"),
              Input({"type":"date_picker","index":ALL},"end_date")
              )
def interval_defaults(tickers,button_clicks,buttons,start_dates,end_dates):
    ctx = dash.callback_context
    callback_id = ctx.triggered[0]['prop_id'].split(".")[0]
    periods = ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y"]
    periods = list(reversed(periods))
    options = ["1m","2m","5m","15m","30m","60m","90m","1d","5d","1wk","1mo","3mo"]
    options_in_minutes = [1,2,5,15,30,60,90,1440,5*1440,7*1440,31*1440,89*1440]
    periods_in_days = [1,5,28,89,365,2*365,5*365,10*365]
    periods_in_days = list(reversed(periods_in_days))
    new_interval_choices = []
    new_full_options_list = []
    for i,ticker in enumerate(tickers):
        if "start_date" in callback_id or "end_date" in callback_id:
            df = yf.Ticker(ticker_dict[ticker]).history(start = start_dates[i],end = end_dates[i])
            start_date = start_dates[i]
            end_date = end_dates[i]
        elif ("period_btn" in callback_id and i*11 < eval(callback_id)["index"] < (i+1)*11) or any(button_clicks[i*11:(i+1)*11]):
            button_name = "max" if not "period_btn" in callback_id else buttons[eval(callback_id)["index"]]
            df = yf.Ticker(ticker_dict[ticker]).history(period=button_name)
            df = df.rename_axis("Date").reset_index()
            x_data = df["Date"]
            start_date = x_data[0] if x_data[0] > datetime.strptime("1970-01-01","%Y-%m-%d") else datetime.strptime("1970-01-01","%Y-%m-%d")
            end_date = x_data[len(x_data)-1]
            start_dates[i] = start_date
            end_dates[i] = end_date
        delta_minutes = (end_date-start_date).days*1440
        options_list = []
        first_index = 100
        for a in range(len(options)):
            if a == 0 and delta_minutes/1440 < 7 and 1 < delta_minutes/options_in_minutes[a] <= 5000:
                options_list.append(options[a])
            elif 0 < a < 7 and delta_minutes/1440 <= 60 and 1 < delta_minutes/options_in_minutes[a] <= 5000:
                options_list.append(options[a])
            elif a >= 7 and 1 < delta_minutes/options_in_minutes[a] <= 5000:
                first_index = a if a < first_index else first_index
                options_list.append(options[a])
        new_interval_choices.append(options_list[0])
        new_full_options_list.append(options_list)
    return new_interval_choices,new_full_options_list,start_dates,end_dates
    
@app.callback(
    Output("graph","figure"),
    Input( {"type":"ticker","index":ALL},"title"),
    Input( {"type":"axis","index":ALL},"value"),
    Input( {"type":"transform","index":ALL},"value"),
    Input( {"type":"line_type","index":ALL},"value"),
    Input( {"type":"date_picker","index":ALL},"start_date"),
    Input( {"type":"date_picker","index":ALL},"end_date"),
    Input( {"type":"interval_select","index":ALL},"value"))
def display_ticker(ticker_indexes,axis_selections,transform_selections,line_selections,start_dates,end_dates,intervals):
    print("indexes",ticker_indexes,"axis",axis_selections,"transform",transform_selections,"line",line_selections,"start",start_dates,"end",end_dates,"intervals",intervals)
    fig = plotly.subplots.make_subplots(specs=[[{"secondary_y":True}]],vertical_spacing=0.5)
    fig.update_layout(margin = dict(r = 0,l = 0, t = 0, b = 0, pad = 0),legend = dict(yanchor = "top",y = 1.1,xanchor = "center",x = 0.5,orientation = "h"),
    xaxis=dict(
        rangeslider=dict(
            visible=True,
            thickness = 0.1,
            yaxis = dict(rangemode = "auto")
        ),
        type="date",
        rangebreaks=[
            ]
    ))
    for i,ticker_index in enumerate(ticker_indexes):
        ticker = full_ticker_list[int(ticker_index)]
        df = yf.Ticker(ticker_dict[ticker]).history(start = start_dates[i][:10],end = end_dates[i][:10],interval = intervals[i])
        df = df.rename_axis("Date").reset_index()
        x_data = df["Date"]
        y_data = df["Close"]
        x_axis = 'x'
        second_y = False
        fill = None
        line_type = line_selections[i]
        if line_type == "Area":
            fill = "tozeroy" if i == 0 else "tonexty"
        transform_selection = transform_selections[i]
        transform_dict = {"Level":(lambda y: y),
                        "Natural Log":(lambda y: np.log(y)),
                        "Change":(lambda y: [y[x]-y[x-1] for x in range(1,len(y))]),
                        "%Change": ( lambda y: [(y[x]-y[x-1])/y[x-1] for x in range(1,len(y))]),
                        "Cumulative": (lambda y: [y[x]-y[0] for x in range(len(y))]),
                        "%Cumulative": (lambda y: [(y[x]-y[0])/y[0] for x in range(len(y))])}
        y_data = transform_dict[transform_selection](y_data)
        x_data = x_data[1:] if transform_selection == "Change" or transform_selection == "%Change" else x_data
        if line_type == "Candle":
            open_data = transform_dict[transform_selection](df["Open"])
            high_data = transform_dict[transform_selection](df["High"])
            low_data = transform_dict[transform_selection](df["Low"])
        if len(ticker_indexes) > 1:
            if "Secondary Y-axis" in axis_selections[i]:
                second_y = True
            if "Secondary X-axis" in axis_selections[i]:
                fig.update_layout(xaxis2= dict(anchor = ('y' if not second_y else 'y2'), overlaying =  'x',side = 'top', 
                rangeslider=dict(
                visible=True,
                thickness = 0.05,
                yaxis = dict(rangemode = "auto"),),
                type="date"),
                yaxis_domain=[0, 0.94],
                xaxis2_type = "date",xaxis_rangeslider_borderwidth = 35,xaxis_rangeslider_bordercolor = "white",xaxis_rangeslider_thickness = 0.05)
                x_axis = 'x2'
        if line_type != "Candle":
            fig.add_trace(go.Scatter(x = x_data,y = y_data,mode = "lines",name = ticker,xaxis = x_axis,fill = fill),secondary_y=second_y)
        else:
            fig.add_trace(go.Candlestick(close = y_data,open = open_data,high=high_data,low = low_data,name = ticker,xaxis = x_axis))
        fig.data[i].update(xaxis = x_axis)       
    return fig          
app.run_server(debug=True)