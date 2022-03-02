import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd
from altair import datum
alt.data_transformers.enable('default', max_rows=None)

# import data
raw_df = pd.read_csv("data/raw/olympics_data.csv", index_col = 0)

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    dcc.RadioItems(
        id='season',
        options=[
            {'label': 'Summer', 'value': 'Summer'},
            {'label': 'Winter', 'value': 'Winter'},
            {'label': 'All', 'value': 'All'}],
        value='All'),
    dcc.Checklist(
        id='medal_type',
        options=[
            {'label': 'Gold', 'value': 'Gold'},
            {'label': 'Silver', 'value': 'Silver'},
            {'label': 'Bronze', 'value': 'Bronze'}],
        value=['Gold', 'Silver', 'Bronze']),
    html.Iframe(
        id='line',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    # dcc.Store stores the intermediate value
    dcc.Store(id='filter_df')
    ])