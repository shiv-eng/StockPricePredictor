# app.py
import yfinance as yf
import dash
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Stock Price Predictor'

# Layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(html.H1("Stock Price Predictor"), width={"size": 6, "offset": 3}),
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Input(
                    id='stock-input',
                    type='text',
                    value='AAPL',
                    placeholder='Enter Stock Symbol',
                ),
                width={"size": 4, "offset": 4},
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=[
                        dcc.Graph(id='stock-chart'),
                        html.Div(id='prediction-output'),
                    ],
                ),
            ),
        ),
    ],
)

# Callbacks
@app.callback(
    [Output('stock-chart', 'figure'), Output('prediction-output', 'children')],
    [Input('stock-input', 'value')],
)
def update_chart(stock_symbol):
    if not stock_symbol:
        raise PreventUpdate

    try:
        stock_data = yf.download(stock_symbol, start="2022-01-01", end="2022-12-31")
        stock_data['Date'] = stock_data.index
        return (
            {
                'data': [
                    {'x': stock_data['Date'], 'y': stock_data['Close'], 'type': 'line', 'name': stock_symbol},
                ],
                'layout': {
                    'title': f'{stock_symbol} Stock Price',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Stock Price (USD)'},
                },
            },
            None,
        )
    except Exception as e:
        return {}, f"Error: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)
