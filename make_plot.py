import numpy as np
import altair as alt
import vega_datasets
import pandas as pd
from data_wrangling import *

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
   
    if y1 =='std':
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
            width=400,
            height=400,
            title = 'SD of Ten Most Stable Jobs from 1850 to 2000'
        )

        # scatter plot, modify opacity based on selection
        line = alt.Chart(first).mark_line().encode(
            alt.X(x2, title = 'Year', axis=alt.Axis(labelAngle=0)),
            alt.Y(y2, title = 'Percentage in Total Work Force'),
            color = 'job',
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        ).properties(
            width=400,
            height=400,
            title = 'Popularity of Ten Most Stable Jobs Over Time'
        )

    if y1 == 'together_y':
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
            width=400,
            height=400,
            title = 'Ten Most Popular Jobs in Year 2000'
        )

        # scatter plot, modify opacity based on selection
        line = alt.Chart(all2).mark_line().encode(
            alt.X('year_x:O', title = 'Year', axis=alt.Axis(labelAngle=0)),
            alt.Y('together_x', title = 'Percentage in Total Work Force'),
            color = 'job',
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        ).properties(
            width=400,
            height=400,
            title = "Popularity Trend of 2000's Ten Most Popular Jobs"
        )
    if z == 'both':
        return (bar | line)
    if z == 'bar':
        return bar