import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import json

#wczytanie mapy
with open('custom.geo.json') as response:
    countries = json.load(response)

# Wczytanie zbioru
file_path='all.csv'
df=pd.read_csv(file_path)

def formula(df):
    return (8/24*df['Temp']/df['Temp'].max()
            -4.5/24*df['Wilgotność']/df['Wilgotność'].max()
            +5.5/24*df['Wiatr']/df['Wiatr'].max()
            +1.5/24*df['Zaludnienie']/df['Zaludnienie'].max()
            + 2/24*df['Siec drogowa']/df['Siec drogowa'].max()
            +3/24*df['Iglaste ']/df['Iglaste '].max()
            +3/24*df['Zachmurzenie ']/df['Zachmurzenie '].max()
            +5.5/24*df['Dni bez opadow']/df['Dni bez opadow'].max())

#--Definicje--
def mapa():
    x=pd.read_csv('dane_rta(1).csv')
    x['model']=formula(x)
    fig=px.choropleth(df,
                      geojson=countries,
                      locations=df['alpha-3'],
                      locationmode='ISO-3',
                      color=x['model'],
                      color_continuous_scale="Bluered",
                      )
    return fig

#####

##Generowanie wykresów
map_fig=mapa()

app = dash.Dash()
app.config.suppress_callback_exceptions=True

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1-example-graph', children=[
        dcc.Tab(label='Mapa', value='tab-1-example-graph'),
        dcc.Tab(label='Źródła i informacje', value='tab-0-example-graph')
    ]),
    html.Div(id='tabs-content-example-graph')
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-0-example-graph':
        return html.Div([
            html.H1(children='--'),
            html.Div(children='--',style={'fontSize': 20}),
            html.Div(id='lista_r',style={'color': 'blue', 'fontSize': 22}),
        ])

    elif tab == 'tab-1-example-graph':
        return html.Div([
            html.H1(children='Mapa (Auto refresh co 20 sekund)'),
            dcc.Graph(
                id='graph7',
                figure=map_fig
            ),
            html.Button('Refresh', id='button',n_clicks=0),
            dcc.Interval(
                id='interval-component',
                interval=2*10000, # in milliseconds
                n_intervals=0)
        ])

@app.callback(
    Output(component_id='graph7',component_property='figure'),
    Input(component_id='button',component_property='n_clicks'),
    Input('interval-component', 'n_intervals')
)
def addNew(click,n_intervals):
    if click > 0:
        map_fig=mapa()
        return map_fig
    return mapa()

app.run_server(debug=True)
