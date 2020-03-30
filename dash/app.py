# -*- coding: utf-8 -*-
import copy
from urllib.request import urlopen
import plotly.express as px
import json
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

with urlopen('https://raw.githubusercontent.com/rozzaaq/dash/master/IndonesianProvinces.json') as response:
    indonesianProvinces = json.load(response)
dfLuasLahan = pd.read_csv(
    "https://raw.githubusercontent.com/rozzaaq/dash/master/LuasLahanProvinsi20142018.csv", dtype={"No": str})
dfProduksiGKG = pd.read_csv(
    "https://raw.githubusercontent.com/rozzaaq/dash/master/ProduksiPadiProvinsi20142018.csv", dtype={"No": str})
dfProduksiBeras = pd.read_csv(
    "https://raw.githubusercontent.com/rozzaaq/dash/master/ProduksiBerasProvinsi20142018.csv", dtype={"No": str})

dfLuasLahanProvinces = pd.DataFrame(dfLuasLahan)
dfLuasLahanProvinces.drop(dfLuasLahanProvinces.tail(1).index, inplace=True)
figLuasLahan = px.choropleth_mapbox(dfLuasLahanProvinces, geojson=indonesianProvinces, locations='Provinsi', color='2018',
                                    color_continuous_scale="YlOrBr",
                                    range_color=(
                                        dfLuasLahanProvinces['2018'].min(), dfLuasLahanProvinces['2018'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=4, center={"lat": -0.8941929, "lon": 117.8948429},
                                    opacity=0.5,
                                    labels={'No': 'Provinsi',
                                            '2018': 'Luas Lahan'}
                                    )
figLuasLahan.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

luasLahanIndonesia = {'Tahun': ['2014', '2015', '2016', '2017', '2018'],
                      'Luas Lahan': [dfLuasLahan['2014'][34], dfLuasLahan['2015'][34], dfLuasLahan['2016'][34], dfLuasLahan['2017'][34], dfLuasLahan['2018'][34]]
                      }
dfLuasLahanIndonesia = pd.DataFrame(
    luasLahanIndonesia, columns=['Tahun', 'Luas Lahan'])

# figLineChart = px.line(dfLuasLahanIndonesia, x="Tahun", y="Luas Lahan")

figLineChart = go.Figure(data=go.Scatter(
    x=dfLuasLahanIndonesia['Tahun'], y=dfLuasLahanIndonesia['Luas Lahan'], line=dict(color='sandybrown')))
figLineChart.update_layout(
    plot_bgcolor='white',
    height=250,
    xaxis_title='Tahun',
    yaxis_title='Luas Area Lahan (ha)'
)

dfLuasLahanReversed = pd.DataFrame(dfLuasLahan)[::-1]
dfLuasLahanReversed.drop(dfLuasLahanReversed.head(1).index, inplace=True)

figBar = go.Figure()
figBar.add_trace(go.Bar(y=dfLuasLahanReversed['Provinsi'], x=dfLuasLahanReversed['2018'] - dfLuasLahanReversed['2017'],
                        base=0,
                        marker=dict(cmax=(dfLuasLahanReversed['2018'] - dfLuasLahanReversed['2017']).max(),
                                    cmin=(
                                        dfLuasLahanReversed['2018'] - dfLuasLahanReversed['2017']).min(),
                                    color=dfLuasLahanReversed['2018'] -
                                    dfLuasLahanReversed['2017'],
                                    colorscale="RdBu"
                                    ),
                        name='expenses',
                        orientation='h'))
# figBar.add_trace(go.Bar(y=years, x=[300, 400, 700],
#                         base=0,
#                         marker_color='lightslategrey',
#                         name='revenue',
#                         orientation='h'
#                         ))
figBar.update_layout(
    plot_bgcolor='white',
    height=800,
    margin={"r": 0, "t": 30, "l": 0, "b": 0}
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# dropdownOptions = []
# for index, row in df.iterrows():
#     dictOptions = {'label': row['fips'], 'value': row['unemp']}
#     dropdownOptions.append(dict(dictOptions))

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H5(
                'Peta Produksi Gabah Kering, Beras, dan Luas Area Lahan wilayah Indonesia tahun 2018',
                id='Title'
            ),
            dcc.Graph(
                id='map-2018',
                figure=figLuasLahan
            ),
            html.Div([
                html.Div([
                    html.Br(),
                    html.H5(
                        'Total Luas Lahan 2018 (ha)',
                        id='totalLuasLahanTitle'
                    ),
                    html.H5(
                        locale.format(
                            "%d", dfLuasLahan['2018'][34], grouping=True),
                        id='totalLuasLahanValue'
                    )
                ],
                    style={'width': '33%',
                           'display': 'inline-block', 'float': 'left', 'textAlign': 'center'}
                ),
                html.Div([
                    html.Br(),
                    html.H5(
                        'Produksi Gabah Kering 2018 (ton)',
                        id='produksiGKGTitle'
                    ),
                    html.H5(
                        locale.format(
                            "%d", dfProduksiGKG['2018'][34], grouping=True),
                        id='produksiGKGValue'
                    )
                ],
                    style={'width': '33%',
                           'display': 'inline-block', 'float': 'left', 'textAlign': 'center'}
                ),
                html.Div([
                    html.Br(),
                    html.H5(
                        'Produksi Beras 2018 (ton)',
                        id='produksiBerasTitle'
                    ),
                    html.H5(
                        locale.format(
                            "%d", dfProduksiBeras['2018'][34], grouping=True),
                        id='produksiBerasValue'
                    )
                ],
                    style={'width': '33%',
                           'display': 'inline-block', 'float': 'left', 'textAlign': 'center'}
                ),
                html.Div([
                    html.Br(),
                    html.H5(
                        'Luas Area Lahan Tahun 2018 (ha)',
                        id='LineChartTitle'
                    ),
                    dcc.Graph(
                        id='lineChart',
                        figure=figLineChart
                    )
                ],
                    style={'width': '100%',
                           'display': 'inline-block', 'float': 'left'}
                )
            ],
                style={'width': '100%'}
            )
        ],
            style={'width': '70%', 'display': 'inline-block', 'float': 'left'}
        ),

        html.Div([
            html.H5(
                'Perubahan Luas Area Lahan Tahun 2017-2018 (ha)'
            ),
            dcc.Graph(
                id='horizontalBar',
                figure=figBar
            )
        ],
            style={'width': '27%',
                   'display': 'inline-block', 'padding': '0px 20px 20px 20px', 'float': 'left'}
        )
    ])
])


# @app.callback(
#     Output('map-2018', 'figure'),
#     [Input('space-slider', 'value')])
# def update_figure(selected_unemp):
#     filtered_df = df[df.unemp == selected_unemp]
#     traces = []
#     for i in filtered_df.continent.unique():
#         df_by_continent = filtered_df[filtered_df['continent'] == i]
#         traces.append(dict(
#             x=df_by_continent['gdpPercap'],
#             y=df_by_continent['lifeExp'],
#             text=df_by_continent['country'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))

#     return {
#         'data': traces,
#         'layout': dict(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita',
#                    'range': [2.3, 4.8]},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest',
#             transition={'duration': 500},
#         )
#     }


# @app.callback(Output('filter', 'children'),
#               [Input('...', '...')],
# def clean_plot(...):
#     lis=[]
#     for i in ...:
#         lis.append(html.Div(dcc.Graph(
#                                   figure={'data': data_for_i})))
#    return lis

# Click Horzontal Bar
# @app.callback(
#     Output('map-2018', 'figure'),
#     [Input('horizontalBar', 'clickData')])
# def horizontalBarClicked(clickData):
#     indonesianProvincesFiltered = dict(indonesianProvinces)
#     for i in range(len(indonesianProvincesFiltered['features'])):
#         if clickData['points'][0]['y'] != indonesianProvincesFiltered['features'][i]['id']:
#             del indonesianProvincesFiltered['features'][i]
#     figLuasLahan = px.choropleth_mapbox(dfLuasLahanProvinces, geojson=indonesianProvincesFiltered, locations='Provinsi', color='2018',
#                                         color_continuous_scale="YlOrBr",
#                                         range_color=(
#                                             dfLuasLahanProvinces['2018'].min(), dfLuasLahanProvinces['2018'].max()),
#                                         mapbox_style="carto-positron",
#                                         zoom=4, center={"lat": -0.8941929, "lon": 117.8948429},
#                                         opacity=0.5,
#                                         labels={'No': 'Provinsi',
#                                                 '2018': 'Luas Lahan'}
#                                         )

@app.callback(
    [Output('map-2018', 'figure'),
     Output('totalLuasLahanValue', 'children'),
     Output('produksiGKGValue', 'children'),
     Output('produksiBerasValue', 'children')],
    [Input('horizontalBar', 'clickData')])
def horizontalBarClicked(clickData):
    global figLuasLahan
    global dfLuasLahan
    global dfProduksiGKG
    global dfProduksiBeras

    if clickData is not None:
        indonesianProvincesFiltered = copy.deepcopy(indonesianProvinces)
        # return json.dumps(indonesianProvincesFiltered['features'][0]['id'])
        j = 0
        for i in range(len(indonesianProvincesFiltered['features'])):
            if clickData['points'][0]['y'] != indonesianProvincesFiltered['features'][j]['id']:
                del indonesianProvincesFiltered['features'][j]
            else:
                j = 1
        figLuasLahan = px.choropleth_mapbox(dfLuasLahanProvinces, geojson=indonesianProvincesFiltered, locations='Provinsi', color='2018',
                                            color_continuous_scale="YlOrBr",
                                            range_color=(
                                                dfLuasLahanProvinces['2018'].min(), dfLuasLahanProvinces['2018'].max()),
                                            mapbox_style="carto-positron",
                                            zoom=4, center={"lat": -0.8941929, "lon": 117.8948429},
                                            opacity=0.5,
                                            labels={'No': 'Provinsi',
                                                    '2018': 'Luas Lahan'}
                                            )
        figLuasLahan.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return [figLuasLahan,
                locale.format("%d", dfLuasLahan['2018'][dfLuasLahan[dfLuasLahan['Provinsi']
                                                                    == clickData['points'][0]['y']].index.values], grouping=True),
                locale.format("%d", dfProduksiGKG['2018'][dfProduksiGKG[dfLuasLahan['Provinsi']
                                                                        == clickData['points'][0]['y']].index.values], grouping=True),
                locale.format("%d", dfProduksiBeras['2018'][dfProduksiBeras[dfLuasLahan['Provinsi'] == clickData['points'][0]['y']].index.values], grouping=True)]
    else:
        return [figLuasLahan,
                locale.format("%d", dfLuasLahan['2018'][34], grouping=True),
                locale.format("%d", dfProduksiGKG['2018'][34], grouping=True),
                locale.format("%d", dfProduksiBeras['2018'][34], grouping=True)]


if __name__ == '__main__':
    app.run_server(debug=True)
