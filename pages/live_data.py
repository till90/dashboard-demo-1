import dash
from dash import Dash, html, Output, Input, dcc
import dash_daq as daq
import plotly.express as px
from apps import navigation
import dash_bootstrap_components as dbc
from wetterdienst import Wetterdienst
from datetime import datetime

dash.register_page(__name__,path='/live',title="Live Data",description="Viszualize Live Data",image='logo2.png')
API = Wetterdienst(provider="dwd", network="observation")

observation_data = API(
    parameter = ['humidity', 'temperature_air_mean_200', 'temperature_air_mean_005','temperature_dew_point_mean_200'],
    resolution = 'minute_10',
    period='now'
    ).filter_by_station_id(station_id=(917))
df = observation_data.values.all().df.dropna(axis=0).set_index('parameter')
df.loc[['temperature_air_mean_200', 'temperature_air_mean_005','temperature_dew_point_mean_200'], 'value'] = df.loc[['temperature_air_mean_200', 'temperature_air_mean_005','temperature_dew_point_mean_200'], 'value'].subtract(273,15)
df_temp = df.loc[['temperature_air_mean_200', 'temperature_air_mean_005','temperature_dew_point_mean_200'], :]
df_temp.index = df_temp.index.remove_unused_categories()

value_1 = df.loc['temperature_air_mean_200', 'value'].iloc[-1].round(2)
led_temp_1 = daq.LEDDisplay(
    label="°C Air Mean at 200 cm",
    value=f'{value_1}',
    color="blue",
    className = 'led_temp_1'
    
)
value_2 = df.loc['temperature_air_mean_005', 'value'].iloc[-1].round(2)
led_temp_2 = daq.LEDDisplay(
    label="°C Air Mean at 5 cm",
    value=f'{value_2}',
    color="red",
    className = 'led_temp_2'
)
value_3 = df.loc['temperature_dew_point_mean_200', 'value'].iloc[-1].round(2)
led_temp_3 = daq.LEDDisplay(
    label="°C Dew Point Mean at 200 cm",
    value=f'{value_3}',
    color="green",
    className = 'led_temp_3'
)
value_time = df.iloc[-1].date.strftime('%T')
today = df.iloc[-1].date.strftime('%Y-%M-%d')
led_time_1 = daq.LEDDisplay(
    label=f"Time for {today}",
    labelPosition='bottom',
    value=value_time,
    color = 'black'
)

fig_temperature = px.line(df_temp, x='date', y='value', title='Temperatures', color=df_temp.index, labels={'parameter' : 'Parameters'}, template='plotly_dark')
df_hum = df.loc['humidity', :]

value_humidity = df_hum.loc['humidity', 'value'].iloc[-1].round(2)

gauge_humidity = daq.Gauge(
    label="Humidity",
    min = 0,
    max = 100,
    value=value_humidity,
    className= 'gauge_humidity'
)

fig_humidity = px.line(df_hum, x='date', y='value', title = 'Humidity', template='plotly_dark',)

layout = html.Div(
    [
        navigation.navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                led_temp_1,
                                led_temp_2,
                                led_temp_3,
                                led_time_1
                            ], width= 3
                        ),
                        dbc.Col(
                            dcc.Graph(figure=fig_temperature, id = 'graph_temperature'),
                            width = 9
                            
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                gauge_humidity
                            ], width = 3
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(figure=fig_humidity, id = 'graph_humidity')
                            ],
                            width = 9
                        )
                    ]
                )
            ],
            fluid = True
        )
    ],
    className = 'live_data_div'
)
print('l55')
