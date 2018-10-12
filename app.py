# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import geocoder
from datetime import datetime
import forecastio
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from cachetools import cached, TTLCache

# This probably shouldn't be committed
API_KEY = "c5dde0bafce3442350c75b743864339a"

# Picked an arbitrary maxsize and ttl-- modify as needed
weather_cache = TTLCache(maxsize=5, ttl=3600*5)

@cached(weather_cache)
def _get_forecast(location):
    a = geocoder.location(location=location)
    lat = a.latlng[0]
    lng = a.latlng[1]
    forecast = forecastio.load_forecast(API_KEY, lat, lng)

    return forecast

def weather_on(loca):
    forecast = _get_forecast(loca)
    byHour = forecast.hourly()
    return byHour

def weather_latest(loca):
    forecast = _get_forecast(loca)
    this = forecast.currently().d
    return this

def get_summary(byhour):
    return byhour.summary

def get_data_24h(byhour):
    temp = []
    date = []
    for hourlyData in byhour.data:
        temp.append(hourlyData.temperature)
        date.append(hourlyData.time)
    return temp, date

def get_data_24h_clo(byhour):
    clo = []
    date = []
    for hourlyData in byhour.data:
        clo.append(hourlyData.d['cloudCover'])
        date.append(hourlyData.time)
    return clo, date

def get_data_24h_pre(byhour):
    clo = []
    date = []
    for hourlyData in byhour.data:
        clo.append(hourlyData.d['precipProbability'])
        date.append(hourlyData.time)
    return clo, date

def get_data_24h_in(byhour):
    clo = []
    date = []
    for hourlyData in byhour.data:
        clo.append(hourlyData.d['precipIntensity'])
        date.append(hourlyData.time)
    return clo, date

app = dash.Dash()
app.title = 'Weather || Astrool'
image_filename = 'logo.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
static_image_route = 'Icons/'

app.layout = html.Div([
    html.Link(rel="shortcut icon", href="favicon.ico"),
    html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={
                    'width': '20%',
                    'margin-left': '40%',
                    'margin-right': 'auto'
                },
             ),
    html.H1(
            children='Astrool-Weather',
            style={
                'textAlign': 'center'
            }
        ),
    html.H3(
            children='Minimal weather app for Astronomers in a hurry! ',
            style={
                'textAlign': 'center'
            }
        ),

    html.H3(
            children='Enter the city name of choice! and press Submit!',
            style={
                'textAlign': 'center'
            }
        ),
    dcc.Input(id='input-1-state', type='text', value='Mandi',style={
        'margin-left': '43%',
        'margin-right': 'auto'
    },),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.H3(
            children='Weather Report for the asked location: ',
            style={
                'textAlign': 'center'
            }
        ),
    html.Div(id='output-state'),
    html.P('     '),
    html.P('     '),
    html.Img(id='image',style={
        'margin-left': '47%',
        'margin-right': 'auto'
    },),
    html.P('     '),
    html.H3(id='output_we',
            style={
                'textAlign': 'center'
            }),
    html.P('     '),
    html.H2(id='output_we1',
            style={
                'textAlign': 'center'
            }),
    html.P('     '),
    # html.H2(style={'textAlign': 'center'}, children='Current Temperature:'),
    html.H2(id='temp',
            style={
                'textAlign': 'center',
                'color': 'blue'
            }),
    html.H2(id='precip',
            style={
                'textAlign': 'center',
                'color': 'red'
            }),
    html.H2(id='h',
            style={
                'textAlign': 'center',
                'color': 'green'
            }),
    html.H1(
            children='7 Day Forecast',
            style={'textAlign': 'center'
                }
        ),
    html.Div(id='table',
            style={
                'textAlign': 'center',
            }),
    html.H1(
            children='Visualisations to help understand: ',
            style={
                'textAlign': 'center'
            }
        ),
    html.H3(
            children='1) Plot of Variation of Temperature in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    dcc.Graph(
        id='first_graph',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H3(
            children='2) Plot of Variation of Cloud Cover in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    dcc.Graph(
        id='first_graph1',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H3(
            children='3) Plot of Variation of Precipitation Probability in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    html.H4(
            children='You can go out taking your telescope on the time where the graph is at 0.',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'red'
            }
        ),
    dcc.Graph(
        id='first_graph2',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H3(
            children='4) Plot of Variation of Precipitation Intensity in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    dcc.Graph(
        id='first_graph3',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H4(
            children='Credits: Akshita Jain - @akshita0208 on GitHub',
            style={
                'textAlign': 'center',
                'color':'red'
            }
        ),
    html.H4(
            children='Copyright © 2018 - Shreyas Bapat(@shreyasbapat) ',
            style={
                'textAlign': 'center',
                'color':'red'
            }
        ),
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_output(n_clicks, input1):
    return None

def ret_str(val):
    return weather_on(val).icon

def ret_sum(val):
    return get_summary(weather_on(val))

def ret_temp(val):
    return weather_latest(val)['temperature']

def ret_pre(val):
    return weather_latest(val)['precipProbability']

def ret_h(val):
    return weather_latest(val)['humidity']

def ret_tup(val):
    return get_data_24h(weather_on(val))

def ret_tup2(val):
    return get_data_24h_clo(weather_on(val))

def ret_tup3(val):
    return get_data_24h_pre(weather_on(val))

def ret_tup4(val):
    return get_data_24h_in(weather_on(val))

@app.callback(Output('image', 'src'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_image_src(n_clicks, value):
    image_filename = static_image_route + ret_str(value) + '.png'
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(Output('output_we', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg1(n_clicks, value):
    stringo = ret_str(value)
    return stringo

@app.callback(Output('output_we1', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg(n_clicks, value):
    stringo = "Summary: " + ret_sum(value)
    return stringo

@app.callback(Output('temp', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg2(n_clicks, value):
    stringo = str(ret_temp(value))
    stringo = "Current Temperature: " + stringo + "℃"
    return stringo

@app.callback(Output('precip', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg3(n_clicks, value):
    stringo = str(ret_pre(value))
    stringo = "Probablilty of Rain: " + stringo
    return stringo

@app.callback(Output('table', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def table(n_clicks, value):
    f = _get_forecast(value)
    dates = [str(d.time.date()) for d in f.daily().data]
    summary = [d.summary for d in f.daily().data]

    return html.Table([html.Tr([html.Th(d) for d in dates[:7]])] + 
            [html.Tr([html.Td(s) for s in summary[:7]])])

@app.callback(Output('h', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg4(n_clicks, value):
    stringo = str(ret_h(value))
    stringo = "Humidity: " + stringo
    return stringo

@app.callback(Output('first_graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra(n_clicks, value):
    a,b = ret_tup(value)
    d = {
        'data' : [
            {
                'x' : b,
                'y' : a,
                'name' : 'Temperature Data for 24 hours'
            }
        ]
    }
    return d

@app.callback(Output('first_graph1', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra1(n_clicks, value):
    a,b =  ret_tup2(value)
    d = {
        'data' : [
            {
                'x' : b,
                'y' : a,
            }
        ]
    }
    return d

@app.callback(Output('first_graph2', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra1(n_clicks, value):
    a,b =  ret_tup3(value)
    d = {
        'data' : [
            {
                'x' : b,
                'y' : a,
            }
        ]
    }
    return d

@app.callback(Output('first_graph3', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra1(n_clicks, value):
    a,b =  ret_tup4(value)
    d = {
        'data' : [
            {
                'x' : b,
                'y' : a,
            }
        ]
    }
    return d

if __name__ == '__main__':
    app.run_server(debug=True)
