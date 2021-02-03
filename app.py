# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
from datetime import date
import dash_html_components as html
import pandas as pd
import yfinance as yf
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

def get_data (stockSymbol, startDt, endDt) :
    if stockSymbol != "":
        stock_df = yf.download(stockSymbol,start=startDt,end=endDt,progress=False,interval='5m')
        stock_df.reset_index(inplace=True,drop=False)
        stock_df['Datetime'] 
        stock_df = stock_df.sort_values(by=["Datetime"], ascending=False)
        returnValue = generate_table(stock_df.head(100))
        #returnValue = html.H4(startDt + ", " + endDt + ", " + stockSymbol)
    else:
        returnValue = html.H4("Please enter the symbol")
    return returnValue
    
    

def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

today = date.today()


app.layout = html.Div([
    
    dcc.Input(
    placeholder='Enter a stock Symbol',
    id='input-box',
    type='text',
    value=''
    ),

    html.Div(dcc.DatePickerRange(
        id='date-picker-range',
        #start_date=date(2020, 12, 1),
        min_date_allowed=datetime.date.today() + datetime.timedelta(-60),
        start_date=datetime.date.today() + datetime.timedelta(-30),
        #end_date=date(int(today.strftime("%Y")), int(today.strftime("%m")), int(today.strftime("%d"))),
        end_date=datetime.date.today(),
        #max_date_allowed=date(int(today.strftime("%Y")), int(today.strftime("%m")), int(today.strftime("%d"))),
        max_date_allowed=datetime.date.today(),
        end_date_placeholder_text='Select a date!'
    )),

    html.Div(html.Button('Submit', id='button')),

    html.Div(id='output-container-button',
             children='Enter a value and press submit')
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, start_date, end_date, value):
    return get_data(value,start_date,end_date)


if __name__ == '__main__':
    app.run_server(debug=True)
