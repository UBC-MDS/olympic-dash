from re import X
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import os
alt.data_transformers.disable_max_rows()


# import data
# absolute path to this file
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
dir_of_interest = os.path.join(PARENT_DIR, 'data')


raw_df = pd.read_csv(f"{dir_of_interest}/raw/olympics_data.csv", index_col = 0)

# list of the top 20 events
top20_events = (raw_df
                .groupby("sport")
                .count()['id']
                .sort_values(ascending=False)
                .head(20)
                .index
                .tolist())

# Creating the objects of the dashboard

season_checkbox = dcc.RadioItems(
            id='season',
            options=[
                {'label': 'Summer', 'value': 'Summer'},
                {'label': 'Winter', 'value': 'Winter'},
                {'label': 'All', 'value': 'all'}],
            value='all',
            labelStyle={'display': 'block'})

medal_checklist = dcc.Checklist(
            id='medal_type',
            options=[
                {'label': 'Gold', 'value': 'Gold'},
                {'label': 'Silver', 'value': 'Silver'},
                {'label': 'Bronze', 'value': 'Bronze'}],
            value=['Gold', 'Silver', 'Bronze'],
            labelStyle={'display': 'block'})

bubble_plot = html.Div([
    html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '140%', 'height': '420px'})
])

height_hist = html.Iframe(
                id='height_hist',
                style={'border-width': '0', 'width': '140%', 'height': '420px'})

year_slider = dcc.Slider(id='medals_by_country',
                value=2000,
                min=1896,
                max=2016,
                step=2,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True})

age_hist = html.Iframe(
                id='age_hist',
                style={'border-width': '0', 'width': '140%', 'height': '420px'})

age_slider = dcc.RangeSlider(id='age_slider',
                min=0,
                max=75,
                step=1,
                value=[0, 75],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True})

line_plot = html.Iframe(
                id='line',
                style={'border-width': '0', 'width': '140%', 'height': '420px'})

## Setup app and layout/frontend
#app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            # dcc.Store stores the intermediate value
            dcc.Store(id='filter_df'),

            # actual layout
            html.H1("Olympics Dashboard"),
            dbc.Col([
                dbc.Row([
                    html.H3("Season"),
                    season_checkbox
                ], align="start"),
                dbc.Row([
                    html.H3("Medal Type"),
                    medal_checklist,
                ], align="center"),
                dbc.Row([
                    html.H3("Year"),
                    year_slider,
                ], align="end"),
            ], width=1.5)
        ]),
        dbc.Col([
            dbc.Spinner(children = bubble_plot, color="primary"),
            dbc.Spinner(children = height_hist, color="success")
        ]),
        dbc.Col([
            dbc.Spinner(children = age_hist, color="warning"),
            age_slider,
            dbc.Spinner(children = line_plot, color="danger"),
        ]),
    ]),
])

# dcc.Store stores the intermediate value
dcc.Store(id='filter_df')

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
                x = alt.X('athletes', title = 'Athletes'),
                y = alt.Y('ave_metals', title = 'Ave. Metals per Athlete'),
                size = alt.Size('metal_count', legend=alt.Legend(
                    orient='top',
                    title='Total Medal Count'
                    )
                ),
                tooltip='noc'
            ).interactive()
        
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
            x=alt.X('height', bin=alt.Bin(maxbins=20), title="Athlete Height"),
            y=alt.Y('count()',title="Count")
            ).add_selection(
                event_select
            ).transform_filter(
                event_select
            ).properties(title="Athlete Height Distribution"
            )
        
        return chart.to_html()

@app.callback(
    Output('age_hist', 'srcDoc'),
    Input('filter_df', 'data'),
    Input('age_slider', 'value'),
    Input('medals_by_country', 'value'),
    Input('medal_type', 'value'))
def plot_altair(filter_df, age_slider, medals_by_country, medal_type):
    
        temp = pd.read_json(filter_df)
        minage = int(age_slider[0])
        maxage = int(age_slider[1])
        year = int(medals_by_country)

        temp = temp[temp['year'] == year]
        temp = temp[temp['age'].between(minage, maxage)]
        temp["order"] = temp["medal"].replace({ 'Bronze' : 1, 'Silver' : 2, 'Gold' : 3 })
        if type(medal_type) != list:
            temp = temp[temp['medal'] == medal_type]

        chart = alt.Chart(temp).mark_area(
                    interpolate='step'
                ).encode(
                    alt.X('age:Q', bin=alt.Bin(maxbins=100), title = "Athlete age range"),
                    alt.Y('count()', title = "Medals Earned"),
                    alt.Color('medal:N',
                            sort=["Gold", "Silver", "Bronze"],
                            scale=alt.Scale(
                                        domain=['Bronze', 'Silver', 'Gold'],
                                        range=['#CD7F32', '#C0C0C0', '#FFD700'])),
                    order=alt.Order('order', sort='ascending')
                ).properties(
                    title='Olympic medals earned by age group')
        return chart.to_html()

@app.callback(
    Output('line', 'srcDoc'),
    Input('filter_df', 'data'))
def plot_altair(filter_df):
    line_chart_df = pd.read_json(filter_df)
    # Get NOC list
    nocs = line_chart_df[["noc"]].values.ravel()
    unique_noc = pd.unique(nocs).tolist()
    unique_noc_sorted = sorted(unique_noc)

    chart_base = alt.Chart(line_chart_df).mark_line().encode(
        x=alt.X('year', title="Year"),
        y=alt.Y("count()", title = 'Count of Medals')
    ).properties(title="Medals Earned Over Time")

    genre_dropdown = alt.binding_select(options=unique_noc_sorted)
    genre_select = alt.selection_single(fields=['noc'], bind=genre_dropdown, name="Country")

    chart = chart_base.add_selection(
        genre_select
    ).transform_filter(
        genre_select
    )

    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
