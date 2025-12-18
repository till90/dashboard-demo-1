import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from apps import navigation

import pandas as pd
from urllib.request import urlopen

import matplotlib.pyplot as plt
from matplotlib.dates import num2date
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

dash.register_page(__name__,path='/weather',title="Weather Data",description="Viszualize and Download Weather Data from different Stations",image='logo2.png')

import warnings
warnings.filterwarnings("ignore")

from wetterdienst import Wetterdienst
API = Wetterdienst(provider="dwd", network="observation")

PATH_DWD_STATIONS = "datasets/misc/dwd_stations.txt"
PATH_DWD_PARAMETER = "datasets/misc/wetterdienst_parameters.txt"
DROPDOWN_STATIONS = "dropdown-stations"
DROPDOWN_RESOLUTION = "dropdown-resolutions"
DROPDOWN_PARAMETER = "dropdown-parameter"
DATE_PICKER_WEATHER = "date-picker-weather"
START_TIME_PICKER_WEATHER = "start-time-picker-weather"
STOP_TIME_PICKER_WEATHER = "stop-time-picker-weather"
WEATHER_PLOTS = "weather-plots"

df_wetterdienst = pd.read_csv(PATH_DWD_PARAMETER, index_col='parameter')
df_wetterdienst_stations = pd.read_csv(PATH_DWD_STATIONS)

layout_user_choices = dbc.Container(
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Station"),
            dcc.Dropdown(
                id  = DROPDOWN_STATIONS,
                options = df_wetterdienst_stations.Stationsname,
                value = 'Darmstadt',
                searchable = True,
            )], width= 2
        ),
        dbc.Col([
            dbc.Label("Select Resolution"),
            dcc.Dropdown(
                id  = DROPDOWN_RESOLUTION,
                options = df_wetterdienst.columns,
                value = 'minute_1',
                searchable = True,
            )], width= 2
        ),
        dbc.Col([
            dbc.Label("Select Parameter"),
            dcc.Dropdown(
                id  = DROPDOWN_PARAMETER,
                options = [],
                placeholder= 'Choose resolution',
                searchable = True,
                multi = True,
            )], width= 4
        ),
        dbc.Col([
            dbc.Label("Select Date"),
            dcc.DatePickerSingle(
                id=DATE_PICKER_WEATHER,
            )], width= 1
        ),
        dbc.Col([
            dbc.Label("Start Time"),
            dcc.Dropdown(
                options = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
                value = "00:00",
                id=START_TIME_PICKER_WEATHER,
            )], width= 1
        ),
        dbc.Col([
            dbc.Label("Stop Time"),
            dcc.Dropdown(
                options = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00","14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
                value = "23:00",
                id=STOP_TIME_PICKER_WEATHER,
            )], width= 1
        )
    ]),
    fluid = True
)


layout_plots = dbc.Container(
    dbc.Row(
        dbc.Col([
            dbc.Label("Plots"),
            html.Div(
                id = WEATHER_PLOTS
            )]
        )
    ),
    fluid=True
)

layout = html.Div(
    [
        navigation.navbar,
        layout_user_choices,
        layout_plots
        
    ]
)

@dash.callback(
    Output(DROPDOWN_PARAMETER, 'options'),
    Input(DROPDOWN_RESOLUTION, 'value')
)
def update_options_parameter(value):
    if not value:
        raise PreventUpdate
    options = df_wetterdienst[value].dropna().index.to_list()
    return options

@dash.callback(
    Output(WEATHER_PLOTS, "children"),
    [
        Input(DROPDOWN_STATIONS, "value"),
        Input(DROPDOWN_RESOLUTION, "value"),
        Input(DROPDOWN_PARAMETER, "value"),
        Input(DATE_PICKER_WEATHER, "date"), 
        Input(START_TIME_PICKER_WEATHER, "value"),
        Input(STOP_TIME_PICKER_WEATHER, "value"),
    ]
)
def update_weather(station, resolution, parameter, date, start_time, stop_time):
    if station is not None and resolution is not None and parameter is not None and date is not None:
        station_id = df_wetterdienst_stations[df_wetterdienst_stations.Stationsname == station].Stations_id.values
        try:
            # Create Request
            observation_data = API(
                parameter=parameter,
                resolution=resolution,
                start_date=f"{date} {start_time}",
                end_date=f"{date} {stop_time}"
                ).filter_by_station_id(station_id=(station_id))
            # Request data as df from API
            df = observation_data.values.all().df.dropna(axis=0).set_index('parameter')
            temp_list = [x for x in parameter if "temp" in x]
            for x in temp_list:
                df.loc[x, 'value'] = df.loc[x, 'value'].subtract(273)
            # Create Figure with subplots
            if len(parameter) > 1:
                fig = make_subplots(
                    rows = len(parameter), 
                    cols = 1,
                    subplot_titles= parameter,
                    shared_xaxes=True,)
            # Get yaxis title from external df
            for n, x in enumerate(parameter):
                si_unit = df_wetterdienst.loc[x, resolution]
                si_unit = si_unit.replace("{", "").replace("}", "").split(",")
                dictionary = {}
                for i in si_unit:
                    dictionary[i.split(":")[0].strip('\'').replace("\"", "")] = i.split(":")[1].strip('"\'').replace("'", "")
                si_unit = dictionary['origin']
                if len(parameter) == 1:
                    if x == "precipitation_height":
                        fig = px.bar(df, x = 'date', y = 'value', labels={'value' : si_unit}, template='plotly_dark')
                    else:
                        fig = px.scatter(df, x = 'date', y = 'value', labels={'value' : si_unit}, template='plotly_dark')
                if len(parameter) > 1:
                    df_temp = df.loc[x]
                    if x == "precipitation_height":
                        fig.append_trace(go.Bar(
                            x = df_temp['date'],
                            y = df_temp['value'],
                        ), row = n + 1, col = 1)
                    else:
                        fig.append_trace(go.Scatter(
                            x = df_temp['date'],
                            y = df_temp['value'],
                        ), row = n + 1, col = 1)
                    fig.update_yaxes(title_text=si_unit, row=n+1, col=1)
                fig.update_layout(showlegend=False, autosize=True, height = 700, template='plotly_dark')
            return html.Div(dcc.Graph(figure=fig), id = WEATHER_PLOTS)
        except Exception as e:
            return html.Div(str(e), id = WEATHER_PLOTS) 
    else:
        return html.Div("Missing Choices", id=WEATHER_PLOTS)