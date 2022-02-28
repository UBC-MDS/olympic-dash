from dash import Dash, dcc, html, Input, Output
import pandas as pd
import altair as alt
from vega_datasets import data

# import data
df = pd.read_csv("../data/raw/olympics_data.csv", index_col = 0)

## Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.RadioItems(
            id='season'
            options=[
                {'label': 'Summer', 'value': 'summer'},
                {'label': 'Winter', 'value': 'winter'},
                {'label': 'All', 'value': 'all'}],
            value='all'),
        dcc.Checklist(
            id='medal_type'
            options=[
                {'label': 'Gold', 'value': 'Gold'},
                {'label': 'Silver', 'value': 'Silver'}],
                {'label': 'Bronze', 'value': 'Bronze'}],
            value=list('Gold', 'Silver', 'Bronze'))

        # dcc.Store stores the intermediate value
        dcc.Store(id='filter_df')
    ])

# Set up callbacks/backend
@app.callback(
    Output('filter_df', 'data'),
    Input('season', 'value'),
    Input('medal_type', 'value'))
def data_preprocess(season, medal_type):
    temp_df = df
    filter = pd.DataFrame()

    if season != 'all':
        temp_df = temp_df[temp_df['season'] == season]

    if length(medal_type) > 0:
        temp_df = temp_df[temp_df['medal'].notna()]

        for medal in medal_type:
            temp = temp_df[temp_df['medal'] == medal]
            filter = filter.append(temp)
        
        return filter

    else:
        return temp_df[temp_df['medal'].notna()]

if __name__ == '__main__':
    app.run_server(debug=True)