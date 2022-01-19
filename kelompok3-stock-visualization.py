# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cp-yeCkiR3IwP6bwkVYKf6m_KjBzVlfL

**Kelompok 3**


1.   Agus Adi Pranata (1301184292)
2.   Pieter Edward (1301184479)
3.   Anggota 3
4.   Anggota 4

**Import Library**
"""

from bokeh.plotting import figure, show
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row, widgetbox

import pandas as pd

"""**Load data from excel**"""

data = pd.read_excel("nasdaqStock.xlsx")

data.drop(columns=['Open', 'High', 'Low', 'Close'], inplace=True)

data_stock = data.rename(columns={"Adj Close": "Adj_Close"})

data.index = data.index.map(str)

"""**Set Select Option**"""

# Select sorted by stock name
option = data_stock['Name'].drop_duplicates()

option = list(option.map(str))

# Select 1 for stock 1
select1 = Select(
    options=option,
    title='Select stock 1',
    value=option[0]
)

# Select 2 for stock 2
select2 = Select(
    options=option,
    title='Select stock 2',
    value=option[1]
)

stock1 = select1.value
stock2 = select2.value

"""**Plotting Stock by Volume**"""

data_stock['Date'] = pd.to_datetime(data_stock['Date'])

#new variable for data
stocks1 = data_stock[data_stock['Name'] == stock1]
stocks2 = data_stock[data_stock['Name'] == stock2]

#column data for stock
data1 = ColumnDataSource(stocks1)
data2 = ColumnDataSource(stocks2)

#plot data
plot = figure(x_axis_type='datetime', x_axis_label='Date', y_axis_label='Volume', title='Stock Volume', plot_height=600, plot_width=1200)
plot.grid.grid_line_alpha=0.3

#plot volume and date
plot.line(x='Date', y='Volume', source=data1, color='#A6CEE3', legend_label=stock1)
plot.line(x='Date', y='Volume', source=data2, color='#FB9A99', legend_label=stock2)

plot.legend.location = "top_left"

#add hover
plot.add_tools(HoverTool(tooltips=[("Stock Name", "@Name"),("Volume", "@Volume"),]))

"""**Update Function**"""

def update_plot(attr, old, new):
    stock1 = select1.value
    stock2 = select2.value

    new_stocks1 = data_stock[data_stock['Name'] == stock1]
    new_stocks2 = data_stock[data_stock['Name'] == stock2]

    data1.data = new_stocks1
    data2.data = new_stocks2

"""**Mengatur Select**"""

# if stock selected
select1.on_change('value', update_plot)
select2.on_change('value', update_plot)

"""**Set layout, panel, and tabs**"""

# make layout with widget
layout1 = row(widgetbox(select1, select2,), plot)

# make panel
line_panel = Panel(child=layout1, title='Line Vizualization')

# union panel to be tab
tabs = Tabs(tabs=[line_panel])

curdoc().add_root(tabs)