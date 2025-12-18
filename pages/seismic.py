import dash
from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from apps import navigation

import pandas as pd
import json
from urllib.request import urlopen

import matplotlib.pyplot as plt
from matplotlib.dates import num2date
import plotly.express as px

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
client = Client("BGR")

dash.register_page(__name__,path='/seismic',title="Seismic Data",description="Viszualize and Download Seismic Data from different Stations",image='logo2.png')

NETWORK_DROPDOWN = "network-dropdown"

STATIONS_TABLE = "stations_table"   
STATIONS_TABLE_DISPLAY = "stations_table_display"
STATIONS_TABLE_DIV = "stations_table_div"

EVENTS_TABLE = "events_table"   
EVENTS_TABLE_DISPLAY = "events_table_display"
EVENTS_TABLE_DIV = "events_table_div"

DATE_PICKER = "date-picker"
DATE_PICKER_DISPLAY = "date-picker-display"

START_TIME_PICKER = "start-time-picker"
STOP_TIME_PICKER = "stop-time-picker"

NETWORK_PATH = "datasets/misc/bgr_networks.json"
EVENT_PATH = 'datasets/misc/events.txt'

SEISMIC_PLOT = "seismic-plot"
BUTTON_PLOT_SEISMIC = "buttons-plot-seismic"
BUTTON_DOWNLOAD_SEISMIC = "buttons-download-seismic"

def load_networks(path: str) -> list:
    with open(path, 'r') as f:
        data = json.load(f)
    data_list = [k + ' - ' +  v for k,v in data.items()]
    return data_list

def load_events(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

networks = load_networks(NETWORK_PATH)
events = load_events(EVENT_PATH)

layout_user_choices = dbc.Container(
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Seismic Network"),
            dcc.Dropdown(
                id  = NETWORK_DROPDOWN,
                options = networks,
                value = 'HS - HLNUGNetz',
            )], width= 3
        ),
        dbc.Col([
            dbc.Label("Select Date"),
            dcc.DatePickerSingle(
                id=DATE_PICKER,
            )], width= 1
        ),
        dbc.Col([
            dbc.Label("Select Start Time"),
            dcc.Dropdown(
                options = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
                value = "00:00",
                id=START_TIME_PICKER,
            )], width= 2
        ),
        dbc.Col([
            dbc.Label("Select Stop Time"),
            dcc.Dropdown(
                options = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00","14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
                value = "23:00",
                id=STOP_TIME_PICKER,
            )], width= 2
        ),
        dbc.Col([
            dbc.Label("Create Graphics"),
            dbc.Button(
                "Plot Data", 
                color="primary",
                id = BUTTON_PLOT_SEISMIC,
            )], width= 1
        ),
        dbc.Col([
            dbc.Label("Download Seismic Data"),
            dbc.Button(
                "Download Data", 
                color="success",
                id = BUTTON_DOWNLOAD_SEISMIC,
            )], width= 2
        )
    ]),
    fluid=True
)

layout_plot = dbc.Container(
    dbc.Row(
        dbc.Col([
            dbc.Label("Seismic Plots"),
            html.Div(
                id = SEISMIC_PLOT
            )]
        )
    ),
    fluid=True
)

layout_networks = dbc.Container(
    dbc.Row(
        dbc.Col([
            dbc.Label("Seismic Stations within selected Network"),
            html.Div(
                dash_table.DataTable(
                    id = STATIONS_TABLE
                    ),
                id = STATIONS_TABLE_DIV
            )
        ])
    ),
    fluid=True
)

layout_events = dbc.Container(
    dbc.Row(
        dbc.Col([
            dbc.Label('Click a cell in the table:'),
            html.Div(
                dash_table.DataTable(
                data = events.to_dict('records'),
                columns = [{"name": i, "id": i} for i in events.columns], 
                row_selectable = 'single',
                style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'},
                style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
                style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                id = EVENTS_TABLE), 
            id=EVENTS_TABLE_DIV),
        ])
    ),
    fluid=True
)

layout = html.Div(
    [
    navigation.navbar,
    layout_user_choices,
    layout_networks,
    layout_plot,
    layout_events
    ]
)

@dash.callback(
    Output(SEISMIC_PLOT, "children"),
    [
        Input(DATE_PICKER, "date"), 
        Input(STATIONS_TABLE, "derived_virtual_data"),
        Input(STATIONS_TABLE, "derived_virtual_selected_rows"),
        Input(EVENTS_TABLE, "derived_virtual_data"),
        Input(EVENTS_TABLE, "derived_virtual_selected_rows"),
    ]
)
def update_seismic(date_value, station_data, row_id, event_data, event_row_id):
    if date_value is not None and station_data is not None and row_id is not None and row_id != []:
        df = pd.DataFrame(station_data)
        df = df.iloc[row_id[0]]
        channel = "HHZ"
        location = "*"
        starttime = UTCDateTime(f"{date_value}T00:00:00")
        endtime = UTCDateTime(f"{date_value}T23:59:59")
        try:
            mystream = client.get_waveforms(df.Network, df.Station, location, channel, starttime, endtime)
            _ = plt.figure()
            x = mystream.plot(fig = _).gca().get_children()[0].get_xdata();
            y = mystream.plot(fig = _).gca().get_children()[0].get_ydata();
            x = [num2date(mpldate) for mpldate in x]
            fig = px.line(x = x , y= y)
            
            return html.Div(dcc.Graph(figure=fig), id = SEISMIC_PLOT)
        except Exception as e:
            return html.Div(str(e), id = SEISMIC_PLOT)
    #elif event_data is not None and event_row_id is not None and station_data is not None:
    #    df_events = pd.DataFrame(event_data)
    #    df_events = df_events.iloc[event_row_id[0]]
    #    df_station = pd.DataFrame(station_data)
    # plot all seimic plots within +- 1 houre of event with get waveforms bulk method    
    else:
        return html.Div("Missing Choices", id=SEISMIC_PLOT)

@dash.callback(
    Output(STATIONS_TABLE_DIV, 'children'),
    Input(NETWORK_DROPDOWN, 'value')
)
def load_bgr_table(network):
        short = network.split(' ')[0]
        r = urlopen(f"https://eida.bgr.de/fdsnws/station/1/query?format=text&level=station&network={short}")
        text = r.read().decode('utf-8')
        if short == "HS":
            text_new = text.replace('#', '').replace('|', ',').split('\n')
            text_line = [x.split(',') for x in text_new]
            text_line[0] = ['Network','Station','Latitude','Longitude','Elevation','SiteName','Logger','Messgerät','StartTime','EndTime']
        else:
            text_new = text.replace('#', '').replace(',', '').replace('|', ',').split('\n')
            text_line = [x.split(',') for x in text_new]
            text_line[0] = ['Network','Station','Latitude','Longitude','Elevation','SiteName','StartTime','EndTime']
        df = pd.DataFrame(text_line)
        df.columns = df.iloc[0] 
        df = df[1:-1]
        return dash_table.DataTable(
            data = df.to_dict('records'),
            columns = [{"name": i, "id": i} for i in df.columns], 
            row_selectable = 'single',
            style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            id = STATIONS_TABLE)

@dash.callback(
    Output(STATIONS_TABLE, "style_data_conditional"),
    Input(STATIONS_TABLE, "derived_virtual_selected_rows"),
)
def style_selected_rows(derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    if len(derived_virtual_selected_rows) > 0:
        return [
        {
            'if': {'row_index': derived_virtual_selected_rows[0]},
            'backgroundColor': 'yellow',
            'color' : 'rgb(30, 30, 30)'
        }]
    return no_update

    
@dash.callback(
    Output(EVENTS_TABLE, "style_data_conditional"),
    Input(EVENTS_TABLE, "derived_virtual_selected_rows"),
)
def style_selected_rows_events(derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    if len(derived_virtual_selected_rows) > 0:
        return [
        {
            'if': {'row_index': derived_virtual_selected_rows[0]},
            'backgroundColor': 'yellow',
            'color' : 'rgb(30, 30, 30)'
        }]
    return no_update