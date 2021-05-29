import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


from sklearn.svm import SVR
from model import prediction



def get_stock_price_fig(df):

    fig = px.line(df,
                  x="Date",
                  y=["Close", "Open"],
                  title="Closing and Openning Price vs Date")

    return fig


def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x="Date",
                     y="EWA_20",
                     title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
				[
					html.Div(
							  [
								html.P("Welcome to the Stock Dash App!", className="start"),
								html.Div([
								  # stock code input
								  html.P("Input Stock Name: ",className="stockName"),
								  
								  dcc.Input(type='text',className="inputStockName",id="stockName"),
								  html.Button('check', id='submit-val', n_clicks=0,className="check"),
								]),
								html.Br(),
								html.Div([
								  # Date range picker input
								  html.P("Pick date range: ",className="stockName"),
								  dcc.DatePickerRange(
										id='my-date-picker-range',
										min_date_allowed=dt(1995, 8, 5),
										max_date_allowed=dt.now(),
										initial_visible_month=dt.now(),
										end_date=dt.now().date(),
										className="datePicker",
									),
								  
								],
								className="datepick",),
								html.Br(),
								html.Br(),
								html.Div([
								  # Stock price button
								  # Indicators button
								  # Number of days of forecast input
								  # Forecast button
								  html.Button('Stock Price', id='check-price', n_clicks=0,className="stockPrice"),
								  html.Button('Indicators', id='indicators', n_clicks=0,className="indicators"),
								  html.Br(),
								  html.Br(),
								  html.Br(),
								  dcc.Input(id='noOfDays',value='noOfDays',type='number',className="noOfDays"),
								  html.Button('Forecast', id='forecast', n_clicks=0,className="forecast"),
								  html.Br(),
								  html.Br(),
								  html.Img(src=app.get_asset_url('b1.jfif'),className="pic1"),
								]),
							  ],
							className="container1"),

					html.Div(
							  [
								html.Div(
									  [  # Logo
										html.Img(src=app.get_asset_url('bvsb.jpg'),className="pic2",id="logo"),
										# Company Name
										html.H1("Bull vs Bear",className="companyName",id="cname")
									  ],
									className="header"),
								html.Div( 
									#Description
									"Please enter a valid stock code to get details......",
									id="description", className="decription_ticker"
									),
								html.Br(),
								html.H3("Stock Price of past few days....",className="stockPriceGraph"),
								html.Br(),
								html.Div([
									# Stock price plot
								], id="graphs-content"),
								html.Br(),
								html.H3("Indicator of the Stock....",className="indicatorGraph"),
								html.Br(),
								html.Div([
									# Indicator plot
								], id="main-content"),
								html.Br(),
								html.H3("Stock Price forecast....",className="stockPriceForecastGraph"),
								html.Br(),
								html.Div([
									# Forecast plot
								], id="forecast-content")
								#html.P(className="alert",id="alert")
							  ],
							className="container2")

									],
						className="container"
					)

#for company info
@app.callback(
	[
		Output("logo", "src"),
		Output("cname","children"),
		Output("description","children"),
		Output("check-price","n_clicks"),
		Output("indicators","n_clicks"),
		Output("forecast","n_clicks"),
		
	],
	[
		Input("submit-val","n_clicks"),
	],
	[
		State("stockName","value"),
	]
			)

def update_data(stock_name,stocck_name_click):
	# your function here
	if stock_name==None:

		
		return "https://www.google.com/imgres?imgurl=https%3A%2F%2Fakm-img-a-in.tosshub.com%2Findiatoday%2Fimages%2Fstory%2F202012%2Fstockvault-bull-versus-bear-fi_1200x768.jpeg%3F300OzshJYLGjqxw.7THu55_sQ0ydPpZ3%26size%3D770%3A433&imgrefurl=https%3A%2F%2Fwww.indiatoday.in%2Feducation-today%2Fjobs-and-careers%2Fstory%2F5-skills-needed-to-get-a-job-in-the-stock-market-1746672-2020-12-04&tbnid=pd9-c3ntJjSFdM&vet=12ahUKEwjbnbaG4OzwAhVDnksFHc94BSsQMygRegUIARD0AQ..i&docid=SF8DsTZkLzxTtM&w=770&h=433&q=stock%20market%20images&ved=2ahUKEwjbnbaG4OzwAhVDnksFHc94BSsQMygRegUIARD0AQ","Are you bullish or bearish?","Please enter a valid stock code to get details......",None,None,None
	else:

		if stocck_name_click==None:
			raise PreventUpdate
		else:
			ticker = yf.Ticker(stocck_name_click)
			inf = ticker.info
			df = pd.DataFrame().from_dict(inf, orient="index")
			df=df.T

			#df[['logo_url', 'shortName', 'longBusinessSummary']]
			return df['logo_url'].values[0], df['shortName'].values[0], df['longBusinessSummary'].values[0],None, None, None

			
# for stocks graphs
@app.callback([
    Output("graphs-content", "children"),
		], 
		[
		    Input("check-price", "n_clicks"),
		    Input('my-date-picker-range', 'start_date'),
		    Input('my-date-picker-range', 'end_date')
		], 
			[State("stockName", "value")]
			)
def stock_price(stock_name, start_date, end_date, stock_price_click):
    if stock_name == None:
        return [""]
        #raise PreventUpdate
    if stock_price_click == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(stock_price_click, str(start_date), str(end_date))
        else:
            df = yf.download(stock_price_click)

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]


# for indicators
@app.callback(
	[Output("main-content", "children")],
	[
    Input("indicators", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
	], 
	[State("stockName", "value")]
	)
def indicators(stock_name, start_date, end_date, stock_indicator_click):
    if stock_name == None:
        return [""]
    if stock_indicator_click == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(stock_indicator_click, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]


# for forecast
@app.callback(
		[
			Output("forecast-content", "children"),

		],
          [	
          	Input("forecast", "n_clicks")
          ],
          [
          	State("noOfDays", "value"),
           	State("stockName", "value")
          ]
            )
def forecast(stock_name, no_of_days, stock_forecast_click):
    if stock_name == None:
        return [""]
    if stock_forecast_click == None:
        raise PreventUpdate

    fig = prediction(stock_forecast_click, int(no_of_days) + 1)

    return [dcc.Graph(figure=fig)]


if __name__ == '__main__':
	app.run_server(debug=True)