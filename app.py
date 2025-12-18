import dash
import dash_bootstrap_components as dbc
from dash import html
# stylesheet with the .dbc class

app = dash.Dash(__name__,use_pages=True,external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(children=[
    dash.page_container
])


if __name__ == "__main__":
    app.run_server(debug=True)

