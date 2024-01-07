import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from db.connector import conn
from CRUD.companies import Companies_CRUD
from CRUD.news import News_CRUD
from CRUD.stocks import Stocks_CRUD
from dash.exceptions import PreventUpdate

company = Companies_CRUD(conn())
news = News_CRUD(conn())
stocks = Stocks_CRUD(conn())

JOURNAL_URL = "https://braziljournal.com/"
ids = {"petro_id": 1, "weg_id": 2, "cea_id": 3}

# valores iniciais
company_id = ids["weg_id"]
company_data = company.get_company_data(company_id)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Ações e Notícias"),

    html.Label("Selecione o Ticker da Ação:"),
    dcc.Dropdown(
        id='dropdown-ticker',
        options=[
            {'label': 'PETR4', 'value': '1'},
            {'label': 'WEGE3', 'value': '2'},
            {'label': 'CEAB3', 'value': '3'},
        ],
        value='1',
        multi=False
    ),

    html.Div([
        dcc.Graph(id='candlestick-chart'),
        html.Div(id='news-list')
    ], style={'display': 'flex'}),
])

@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('dropdown-ticker', 'value')]
)
def update_candlestick_chart(company_id):

    company_data = company.get_company_data(company_id)
    company_ticker = company_data[0].ticker
    start_date = '2023-01-01'

    stock_data = stocks.get_stock_data(company_id, company_ticker, start_date)
    df = pd.DataFrame([(stock.dat_data, stock.open_price, stock.max_price, stock.min_price, stock.close_price, stock.adj_close_price) for stock in stock_data],
                      columns=['dat_data', 'open_price', 'high_price', 'low_price', 'close_price', 'adj_close_price'])
    df['dat_data'] = pd.to_datetime(df['dat_data'])
    df.columns = df.columns.str.lower()

    fig_candlestick = go.Figure(data=[go.Candlestick(x=df['dat_data'],
                                                      open=df['open_price'],
                                                      high=df['high_price'],
                                                      low=df['low_price'],
                                                      close=df['close_price'])])

    return fig_candlestick

@app.callback(
    Output('news-list', 'children'),
    [Input('dropdown-ticker', 'value')]
)
def update_news_list(company_id):
    company_cod_search = company_data[0].cod_search
    articles = news.get_news(JOURNAL_URL, company_cod_search, company_id)

    if articles is not None:
        news_list = [html.Div([
            html.A(
                html.H3(news_item['title'], style={'color': 'black'}),
                href=news_item['link'],
                target='_blank'  # Abre em uma nova guia
            ),
            html.P(f"Date: {news_item['dat_data']}") if 'dat_data' in news_item else None,
            html.Hr()
        ]) for news_item in articles]
    else:
        news_list = [html.P("Não foi possível obter as notícias.")]

    return news_list

if __name__ == '__main__':
    app.run_server(debug=True)
