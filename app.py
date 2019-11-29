import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
import altair as alt

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'

def make_plot(x1 = 'job',y1 = 'std',x2 = 'year_x:O',y2 = 'together', z = 'both'):
    # Don't forget to include imports
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default


    # Create a plot from the cars dataset

    data = pd.read_json('https://raw.githubusercontent.com/vega/vega-datasets/master/data/jobs.json')
    data = pd.DataFrame(data)
    import numpy as np
   
    if y1 =='std':
        data['job'] = data['job'].str.replace('Professor.*', 'Professor', regex=True)
        mini_sd = data.groupby(['job']).std().sort_values(by=['perc'], 
                                                    ascending=[True]).reset_index().iloc[:10]
        
        mini_sd = mini_sd.rename(columns = {'perc':'std'})
        all1 = pd.merge(data, mini_sd, how="inner", on="job")
        first = all1.query('sex == "men"')
        second = all1.query('sex == "women"')
        first = first.reset_index()
        first['together'] = pd.Series(np.asarray(first['perc']) + np.asarray(second['perc']))
        first = first.replace({'together' : 0}, value = np.nan)
        first = first.interpolate()
        first = first.sort_values(by=['std'], 
                                ascending=[True])
        first = first.reset_index()
        brush = alt.selection_interval(
        encodings=['x'] # limit selection to x-axis (year) values
        )

        # dynamic query histogram
        bar = alt.Chart(first).mark_bar().add_selection(
            brush
        ).encode(
            alt.X(x1, title='Job', axis=alt.Axis(labelAngle=30)),
            alt.Y(y1, title= 'Standard Diveation')
        ).properties(
            width=500,
            height=500,
            title = 'SD of Ten Most Stable Jobs from 1850 to 2000'
        )

        # scatter plot, modify opacity based on selection
        line = alt.Chart(first).mark_line().encode(
            alt.X(x2, title = 'Year', axis=alt.Axis(labelAngle=0)),
            alt.Y(y2, title = 'Percentage in Total Work Force'),
            color = 'job',
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        ).properties(
            width=500,
            height=500,
            title = 'Popularity of Ten Most Stable Jobs Over Time'
        )

    if y1 == 'together_y':
        first2 = data.query('sex == "men"')
        second2 = data.query('sex == "women"')
        first2 = first2.reset_index()
        first2['together'] = pd.Series(np.asarray(first2['perc']) + np.asarray(second2['perc']))
        first2 = first2.replace({'together' : 0}, value = np.nan)
        first2 = first2.interpolate()
        first2 = first2.sort_values(by=['perc'], 
                                ascending=[True])
        first2 = first2.reset_index()

        first2['job'] = first2['job'].str.replace('Professor.*', 'Professor', regex=True)
        first3 = first2[first2['year'].isin(['2000'])]
        first3 = first3.sort_values(by=['perc'], ascending=[False]).iloc[:10]

        all2 = pd.merge(first2, first3, how="inner", on="job")
        brush = alt.selection_interval(
        encodings=['x'] # limit selection to x-axis (year) values
        )

        # dynamic query histogram
        bar = alt.Chart(all2).mark_bar().add_selection(
            brush
        ).encode(
            alt.X(x1, title='Job', axis=alt.Axis(labelAngle=30)),
            alt.Y(y1, title= 'Percentage')
        ).properties(
            width=500,
            height=500,
            title = 'Ten Most Popular Jobs in Year 2000'
        )

        # scatter plot, modify opacity based on selection
        line = alt.Chart(all2).mark_line().encode(
            alt.X('year_x:O', title = 'Year', axis=alt.Axis(labelAngle=0)),
            alt.Y('together_x', title = 'Percentage in Total Work Force'),
            color = 'job',
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        ).properties(
            width=500,
            height=500,
            title = "Popularity Change Over Time of 2000's Ten Most Popular Jobs"
        )
    if z == 'both':
        return (bar & line)
    if z == 'bar':
        return bar

jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                #html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
                #     width='100px'),
                html.H1("Job Tracker", className="display-3"),
                html.P(
                    "Find interesting features in job from 1850 to 2000 by selecting on charts! (Missing data was estimated by interpolation)",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

logo = dbc.Row(dbc.Col(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
                      width='15%'), width=4))

content = dbc.Container([
    dbc.Row(
                [dbc.Col(
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='800',
                        width='1200',
                        style={'border-width': '0'},
                        ################ The magic happens here
                        srcDoc=make_plot().to_html()
                        ################ The magic happens here
                        ),width=8),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dd-chart-y',
                            options=[
                                {'label': 'Standard Deviation', 'value': 'std'},
                                {'label': 'Percentage in 2000', 'value': 'together_y'}
                                # {'label': '2000', 'value': '2000'},
                                # {'label': 'Horsepower', 'value': 'Horsepower'}
                            ],
                            clearable=False,
                            value='std',
                            # style=dict(width='45%',
                            #         verticalAlign="middle")
                            ), width=2,
                            ),
                    dbc.Col(        
                        dcc.Dropdown(
                        id='dd-chart-x',
                        options=[
                            {'label': 'Job', 'value': 'job'}#,
                            # {'label': 'Cylinders', 'value': 'Cylinders'},
                            # {'label': 'Displacement', 'value': 'Displacement'},
                            # {'label': 'Horsepower', 'value': 'Horsepower'}
                        ],
                        clearable=False,
                        value='job'
                        ), width=2),
                    dbc.Col(        
                        dcc.RadioItems(
                                        id='dd-chart-z',
                                        options=[
                                        {'label': 'Bar Only', 'value': 'bar'},
                                        {'label': 'Both', 'value': 'both'}
                                        ],
                                          value='both'
                                        ), width=2
                    )
                ]
            )
    ]
)

footer = dbc.Container([dbc.Row(dbc.Col(html.P('This Dash app was made collaboratively by the DSCI 532 group 208! /n Trying this one'))),(dbc.Col(html.P('[Second footer](https://www.peanuts.com)')))
         ])
# footer = dbc.Container([dbc.Row(dbc.Col(html.P('[Second footer](https://www.peanuts.com)'))),
#          ])

app.layout = html.Div([jumbotron,
                       content,
                       footer])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart-x', 'value'),
     dash.dependencies.Input('dd-chart-y', 'value'),
     dash.dependencies.Input('dd-chart-z', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name,
                zaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(x1 = xaxis_column_name,
                             y1 = yaxis_column_name,
                             z = zaxis_column_name).to_html()
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)
