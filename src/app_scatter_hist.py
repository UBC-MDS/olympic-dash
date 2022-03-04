from dash import Dash, dcc, html, Input, Output
import pandas as pd
import altair as alt
from vega_datasets import data

# import data
raw_df = pd.read_csv("../data/raw/olympics_data.csv", index_col = 0)

# list of the top 20 events
top20_events = (raw_df
                .groupby("sport")
                .count()['id']
                .sort_values(ascending=False)
                .head(20)
                .index
                .tolist())

## Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        html.Iframe(
            id='height_hist',
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.RadioItems(
            id='season',
            options=[
                {'label': 'Summer', 'value': 'Summer'},
                {'label': 'Winter', 'value': 'Winter'},
                {'label': 'All', 'value': 'all'}],
            value='all'),
        dcc.Checklist(
            id='medal_type',
            options=[
                {'label': 'Gold', 'value': 'Gold'},
                {'label': 'Silver', 'value': 'Silver'},
                {'label': 'Bronze', 'value': 'Bronze'}],
            value=['Gold', 'Silver', 'Bronze']),
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
            filter = filter.append(temp)
        
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
                y = 'athletes',
                x = 'ave_metals',
                size = 'metal_count',
                tooltip='noc').interactive()
        
        return chart.to_html()

@app.callback(
    Output('height_hist', 'srcDoc'),
    Input('filter_df', 'data'),
    Input('medals_by_country', 'value'),
    Input('medal_type', 'value'))
def plot_altair(filter_df, medals_by_country, medal_type):
        temp = pd.read_json(filter_df)
        year = int(medals_by_country)

        temp = temp[temp['year'] == year]
        if type(medal_type) != list:
            temp = temp[temp['medal'] == medal_type]

        event_dropdown = alt.binding_select(options=top20_events)
        event_select = alt.selection_single(fields=['sport'], bind=event_dropdown, name='Olympic')

        chart = alt.Chart(temp).mark_bar().encode(
            x=alt.X('height', bin=alt.Bin(maxbins=20)),
            y='count()'
            ).add_selection(
                event_select
            ).transform_filter(
                event_select
            ).properties(title="Athlete Height Distribution")
        
        return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)