import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd
from altair import datum
alt.data_transformers.enable('default', max_rows=None)

# import data
raw_df = pd.read_csv("../data/raw/olympics_data.csv", index_col = 0)

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

# Set up callbacks/backend
@app.callback(
    Output('filter_df', 'data'),
    Input('season', 'value'),
    Input('medal_type', 'value'))
def data_preprocess(season, medal_type):
    temp_df = raw_df
    filter = pd.DataFrame()

    if season != 'all':
        temp_df = temp_df[temp_df['season'] == season]

    if len(medal_type) > 0:
        temp_df = temp_df[temp_df['medal'].notna()]

        for medal in medal_type:
            temp = temp_df[temp_df['medal'] == medal]
            filter = pd.concat([filter, temp])
        
        return filter.to_json()

    else:
        return temp_df.to_json()

@app.callback(
    Output('line', 'srcDoc'),
    Input('filter_df', 'data'))
def plot_altair(filter_df):
    nocs = raw_df[["noc"]].values.ravel()
    unique_noc = pd.unique(nocs).tolist()
    unique_noc_sorted = sorted(unique_noc)

    line_chart_df = pd.read_json(filter_df)

    chart_base = alt.Chart(line_chart_df).mark_line().encode(
        x='year',
        y=alt.Y("count()", title = 'Count of Medals')
    ).properties(title="Medals Earned Over Time")

    genre_dropdown = alt.binding_select(options=unique_noc_sorted)
    genre_select = alt.selection_single(fields=['noc'], bind=genre_dropdown, name="NOC")

    chart = chart_base.add_selection(
        genre_select
    ).transform_filter(
        genre_select
    )

    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)