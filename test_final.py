# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:39:42 2019

@author: irene
"""

from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np # we will use this later, so import it now
from bokeh.plotting import figure
from bokeh.resources import CDN # Need to be added
from bokeh.io import output_notebook, show
from datetime import datetime
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.embed import components


app_stock = Flask(__name__)
app_stock.vars = {}

@app_stock.route('/hello_stock', methods = ['GET', 'POST'])
def hello_stock():
    if request.method == 'GET':
        return render_template('userinfo_stock.html')
    else:
        app_stock.vars['name_stock'] = request.form['name_stock']
        app_stock.vars['date_from'] = request.form['date_from']
        app_stock.vars['date_to'] = request.form['date_to']
        parameters = {'symbol': app_stock.vars['name_stock'], 'api_token':'a9Fa0I4w1DAvfZIbXS2DlSBTOMIj7ULPpIg496Zw7KYu8zqAvYMS7em2nRHN', 'date_from': app_stock.vars['date_from'],'date_to': app_stock.vars['date_to']}
        
        response = requests.get('https://api.worldtradingdata.com/api/v1/history', params = parameters)
        json_data = response.json()
        data_df = json_data['history']
        
        date = [k for k in data_df]
        open_price = []
        close_price = []
        
        for day in date:
            open_price.append(data_df[day]['open'])
            close_price.append(data_df[day]['close'])
        
        price_df = pd.DataFrame(data = list(zip(date, open_price, close_price)), columns = ['date','open_price','close_price'])
        price_df['date'] = pd.to_datetime(price_df['date'])
        
        ab = figure(x_axis_type="datetime", title="Daily Close Price", plot_height=350, plot_width=800)
        sources = ColumnDataSource(price_df)
        
        ab.xgrid.grid_line_color=None
        ab.ygrid.grid_line_alpha=0.5
        ab.xaxis.axis_label = 'Time'
        ab.yaxis.axis_label = 'Value'
        ab.line('date', 'close_price', source = sources)
        
        hover = HoverTool(tooltips=[('date','@date{%F}'),
                                    ('close price','$@close_price'),
                                    ('open price', '$@open_price')],
                            formatters={'date': 'datetime', 
                                        'close price' : 'printf'}, mode='vline')
        ab.add_tools(hover)
        #cdn_js = CDN.js_files[0]
        #cdn_css = CDN.css_files[0]
        script, div = components(ab)
        #show(ab)
        return render_template('result_stock.html', script = script, div=div)

if __name__ == '__main__':
    app_stock.run(debug=True)

 