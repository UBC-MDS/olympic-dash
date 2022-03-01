from re import X
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import altair as alt

# import data
raw_df = pd.read_csv("../data/raw/olympics_data.csv", index_col = 0)

## Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
        dcc.RadioItems(
            id='season',
            options=[
                {'label': 'Summer', 'value': 'summer'},
                {'label': 'Winter', 'value': 'winter'},
                {'label': 'All', 'value': 'all'}],
            value='all'),
        dcc.Checklist(
            id='medal_type',
            options=[
                {'label': 'Gold', 'value': 'Gold'},
                {'label': 'Silver', 'value': 'Silver'},
                {'label': 'Bronze', 'value': 'Bronze'}],
            value=['Gold', 'Silver', 'Bronze']),
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='medals_by_country',
            value=2000,
            min=1896,
            max=2016,
            step=2,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True}),

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
    Output('scatter', 'srcDoc'),
    Input('filter_df', 'data'),
    Input('medals_by_country', 'value'))
def plot_altair(filter_df, medals_by_country):
        temp = pd.read_json(filter_df)
        year = int(medals_by_country)

        temp = temp[temp['year'] == year]
        athlete_df = raw_df[raw_df['year'] == year]

        df = pd.DataFrame()

        df['athletes'] = athlete_df.groupby(['noc'])['id'].nunique()
        df['metal_count'] = temp.groupby(['noc'])['medal'].count()
        df['ave_metals'] = df['metal_count'] / df['athletes']

        df = df.reset_index()

        chart = alt.Chart(df).mark_circle().encode(
                x = alt.X('athletes', title = 'Number of Athletes'),
                y = alt.Y('ave_metals', title = 'Ave. Metals per Athlete'),
                size = alt.Size('metal_count', title = "Total Metal Count"),
                tooltip='noc'
                ).interactive()
        
        return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)