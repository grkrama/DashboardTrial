# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance as yf
import datetime
from datetime import date

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sketchy/bootstrap.min.css']
#[dbc.themes.LUX]
#https://bootswatch.com/sketchy/
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

def get_data (stockSymbol, startDt, endDt, interval_value) :
    
    if stockSymbol != "":
        stock_df = yf.download(stockSymbol,start=startDt,end=endDt,progress=False,interval=interval_value)
        stock_df.reset_index(inplace=True,drop=False)
        stock_df['Datetime'] 
        stock_df = stock_df.sort_values(by=["Datetime"], ascending=False)
        returnValue = generate_table(stock_df.head(100))
        #returnValue = html.H4(startDt + ", " + endDt + ", " + stockSymbol)
    else:
        returnValue = html.P("Please enter the symbol", className='mb-0')
    return returnValue
    
    

def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns], className='table-primary')
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], className='table table-hover')

today = date.today()


#app.layout = dbc.Container([ 
app.layout = html.Div([   
    html.Div(
        dcc.Input(placeholder='Enter a stock Symbol',
                  id='input-box',
                  type='text',
                  value=''), className='form-group'),


    html.Div(
        dcc.DatePickerRange(
        id='date-picker-range',
        #start_date=date(2020, 12, 1),
        min_date_allowed=datetime.date.today() + datetime.timedelta(-60),
        start_date=datetime.date.today() + datetime.timedelta(-30),
        #end_date=date(int(today.strftime("%Y")), int(today.strftime("%m")), int(today.strftime("%d"))),
        end_date=datetime.date.today(),
        #max_date_allowed=date(int(today.strftime("%Y")), int(today.strftime("%m")), int(today.strftime("%d"))),
        max_date_allowed=datetime.date.today(),
        end_date_placeholder_text='Select a date!'
    ), className='form-group'),

    html.Div(
        
        dcc.Dropdown(
        id='interval-drop-down',
        multi=False,
        value='15m',
        options=[
            {'label': '1 Minute', 'value': '1m'},
            {'label': '5 Minutes', 'value': '5m'},
            {'label': '15 Minutes', 'value': '15m'},
            {'label': '30 Minutes', 'value': '30m'},
            {'label': '60 Minutes', 'value': '60m'},
            {'label': '90 Minutes', 'value': '90m'},
            {'label': '1 Day', 'value': '1d'},
            {'label': '5 Days', 'value': '5d'},
            {'label': '1 Week', 'value': '1wk'},
            {'label': '1 Month', 'value': '1mo'},
            {'label': '3 Months', 'value': '3mo'}
        ],
        placeholder ='Select Interval'
        
    ),className='form-group'),

    html.Select([
            html.Option(
            children='1 Minute',
            id='option-1m',
            value ='1m'
            ),
            html.Option(
            children='5 Minutes',
            id='option-5m',
            value ='5m'
            ),
            html.Option(
            children='15 Minute',
            id='option-15m',
            value ='15m'
            ),
            html.Option(
            children='30 Minutes',
            id='option-30m',
            value ='30m'
            ),
            html.Option(
            children='90 Minute',
            id='option-90m',
            value ='90m'
            ),
            html.Option(
            children='1 Day',
            id='option-1d',
            value ='1d'
            ),
            html.Option(
            children='5 Days',
            id='option-5d',
            value ='5d'
            ),
            html.Option(
            children='1 Week',
            id='option-1wk',
            value ='1wk'
            ),
            html.Option(
            children='1 Months',
            id='option-1mo',
            value ='1mo'
            )
            ,
            html.Option(
            children='3 Months',
            id='option-3mo',
            value ='3mo'
            )
        ]),
    
    html.Div(html.Button('Submit', id='button', className='btn btn-primary')),

    html.Div(id='output-container-button',
             children='Enter a value and press submit', className='form-group')
], style={'margin': 10}, className='jumbotron')


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('interval-drop-down', 'value')
     ],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, start_date, end_date, interval_value, value):
    return get_data(value,start_date,end_date,interval_value)


if __name__ == '__main__':
    app.run_server(debug=True)
