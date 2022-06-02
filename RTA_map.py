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

# Wczytanie zbioru graczy
file_path='all.csv'
df=pd.read_csv(file_path)



#--Definicje--
def mapa():
    x=np.random.random(df.shape[0])
    fig=px.choropleth(df,
                      geojson=countries,
                      locations=df['alpha-3'],
                      locationmode='ISO-3',
                      color=x,
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
def addNew(click,inter):
    if click > 0:
        map_fig=mapa()
        return map_fig
    return mapa()

app.run_server(debug=True)