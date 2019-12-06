import numpy as np
import altair as alt
import vega_datasets
import pandas as pd
from Code.data_wrangling import *

def make_plot(x1 = 'job',y1 = 'std',x2 = 'year_x:O',y2 = 'together', z = 'both'):
    '''
    Make corresponding plots based on the input. Default is make both 
    (bar + line). If 'bar' is input then make bar plot only.


    Parameters
    ----------
    x1: str
        The string that is x axis for bar.
    y1: str
        The string that is y axis for line.
    x2: str
        The string that is x axis for bar for popularity.
    y2: str
        The string that is y axis for linefor popularity.
    z: str
        The string to specify what plot to make
    Returns
    -------
    altair plot 
        A wantted plot.   
    '''
    def mds_special():
        '''
        This is MDS special theme for altair plot
        '''
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
   
    if y1 =='std':
        brush = alt.selection_multi(
        encodings=['x'] # limit selection to x-axis (year) values
        )

        # dynamic query histogram
        bar = alt.Chart(first).mark_bar().add_selection(
            brush
        ).encode(
            alt.X(x1, title='Job', axis=alt.Axis(labelAngle=30),
            sort=alt.EncodingSortField(
            field=y1,  # The field to use for the sort
            order="ascending")),
            alt.Y(y1, title= 'Standard Diveation'),
            color=alt.condition(brush, 'job', alt.value('grey'))
        ).properties(
            width=400,
            height=400,
            title = 'SD of Ten Most Stable Jobs from 1850 to 2000'
        )

        # line plot, modify opacity based on selection
        line = alt.Chart(first).mark_line().encode(
            alt.X(x2, title = 'Year', axis=alt.Axis(labelAngle=0)),
            alt.Y(y2, title = 'Percentage in Total Work Force', axis=alt.Axis(format='%')),
            color = 'job',
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        )
        line_inter = alt.layer(
        line, # base line chart
        
        # add circle marks for selected time points, hide unselected points
        line.mark_circle().encode(
            opacity=alt.condition(brush, alt.value(1), alt.value(0))
        ).add_selection(brush)).properties(
            width=400,
            height=400,
            title = 'Popularity of Ten Most Stable Jobs Over Time'
        )

    if y1 == 'together_y':
        brush = alt.selection_multi(
        encodings=['x'] # limit selection to x-axis (year) values
        )

        # dynamic query histogram
        bar = alt.Chart(all2).mark_bar().add_selection(
            brush
        ).encode(
            alt.X(x1, title='Job', axis=alt.Axis(labelAngle=30),
            sort=alt.EncodingSortField(
            field=y1,  # The field to use for the sort
            order="descending")),
            alt.Y(y1, title= 'Percentage',axis=alt.Axis(format='%')),
            color=alt.condition(brush, 'job', alt.value('grey'))
        ).properties(
            width=400,
            height=400,
            title = 'Ten Most Popular Jobs in Year 2000'
        )

        # scatter line, modify opacity based on selection
        line = alt.Chart(all2).mark_line().encode(
            alt.X('year_x:O', title = 'Year', axis=alt.Axis(labelAngle=0)),
            alt.Y('together_x', title = 'Percentage in Total Work Force',axis=alt.Axis(format='%')),
            color = 'job',
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        )

        line_inter = alt.layer(
        line, # base line chart
        
        # add circle marks for selected time points, hide unselected points
        line.mark_circle().encode(
            opacity=alt.condition(brush, alt.value(1), alt.value(0))
        ).add_selection(brush)).properties(
            width=400,
            height=400,
            title = "Popularity Trend of 2000's Ten Most Popular Jobs"
        )
        
    if z == 'both':
        return  (bar | line_inter)
        
    if z == 'bar':
        return bar