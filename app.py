import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
import altair as alt
from Code.make_plot import *

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'


jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [   html.H1("Job Tracker", className="display-2"),
                html.P(
                    "Find the most stable jobs from 1850 to 2000 and most popular job in 2000 ",
                    className="lead",
                ),
                html.P(
                    "Click the bar you are interested in to visualize that job's trend!(Multiple selection: shift + click)",
                    className="lead",
                ),
                html.P(
                    "Note: Missing data was estimated by interpolation.",
                    className="lead",
                )
                
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
                [   html.Label('Question you are interested :'),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dd-chart-y',
                            options=[
                                {'label': 'Top 10 Stable Jobs', 'value': 'std'},
                                {'label': 'Top 10 Popular Jobs in 2000', 'value': 'together_y'}
                                # {'label': '2000', 'value': '2000'},
                                # {'label': 'Horsepower', 'value': 'Horsepower'}
                            ],
                            clearable=False,
                            value='std',
                            # style=dict(width='45%',
                            #         verticalAlign="middle")
                            ),
                            ),
                    html.Label('Dataset :'), 
                    dbc.Col(       
                        dcc.Dropdown(
                        id='dd-chart-x',
                        options=[
                            {'label': 'Job (From Vega)', 'value': 'job'},
                            {'label': 'More dataset coming soon', 'value': 'job'}#,
                            # {'label': 'Displacement', 'value': 'Displacement'},
                            # {'label': 'Horsepower', 'value': 'Horsepower'}
                        ],
                        clearable=False,
                        value='job'
                        )),
                    html.Label('Chart Type :'),  
                    dbc.Col(      
                        dcc.RadioItems(
                                        id='dd-chart-z',
                                        options=[
                                        {'label': 'Bar Only', 'value': 'bar'},
                                        {'label': 'Bar + Line', 'value': 'both'}
                                        ],
                                          value='bar'
                                        )
                    ),
                    dbc.Col(
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='600',
                        width='1300',
                        style={'border-width': '0'},
                        ################ The magic happens here
                        srcDoc=make_plot().to_html()
                        ################ The magic happens here
                        )),
                ]
            )
    ]
)

footer = dbc.Container([dbc.Row(dbc.Col(html.P('This Dash app was made collaboratively by the DSCI 532 group 208!'))),
    dcc.Markdown(
        '''
        [Data Source](https://github.com/vega/vega-datasets/blob/master/data/jobs.json)
        '''
    )
         ])

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