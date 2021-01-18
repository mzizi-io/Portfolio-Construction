#######################################################################
# Useful functions for data processings, transformations and plotting
#----------------------------------------------------------------------
#TO DO
#-----
#- Treemap
#######################################################################

import numpy as np
import pandas as pd
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def import_data(paths, tickers):
    """
    This function allows to import multiple etfs data and concatenate them in a dataframe. 
	:paths (list) --> list of etfs data paths
	:tickers (list) --> list of etfs tickers sorted according to paths list 
    """
    data = []
    for i in range(len(paths)): 
        etf_data = pd.read_csv(paths[i], sep=';', header=0, names=['DateTime', tickers[i]], index_col='DateTime',
							   parse_dates=False).replace(to_replace=',',value = '.', regex=True).astype(float)
        etf_data.index = pd.to_datetime(etf_data.index, format="%d/%m/%Y")
        data = data + [etf_data]    
    return pd.concat(data, axis=1)


def get_clean_data(data, components= "returns", period="monthly"): 
	"""
	This returns data depending on the type of the inputs (prices or returns) and gets 
	the period per year of the portfolio input data. It outputs the portfolio data with the right format. 
	:components_types (str) <-- {prices, returns}.
	:period (str) <-- {daily, monthly, quaterly}.
	"""
	if period == "monthly":
		period_per_year = 12
	elif period == "daily": 
		period_per_year = 252
	elif period == 'quaterly':
		period_per_year = 4
	else: 
		raise NotImplementedError("Expected period to be 'daily', 'monthly' or 'quaterly'")
		
	if components == 'returns': 
		data = data
	elif components == 'prices': 
		data = data.pct_change(axis=0)
		data = data.dropna(axis=0)  
	else: 
		raise NotImplementedError("Expected components to be prices or returns data")
		
	return period_per_year, data


def plot_risk_estimates_heatmap(correlation_matrix, colorscale, showscale, title): 
	"""
	This function returns the risk estimates matrice heatmap. 
	:correlation_matrix (pd.DataFrame)
	:colorscale (str)
	:showscale (bool)
	:title (str)
	"""
	trace = go.Heatmap(z=correlation_matrix.values,
                   x=correlation_matrix.index,
                   y=correlation_matrix.columns,
                   colorscale=colorscale,
                   showscale=showscale)
	
	layout = dict(xaxis_showticklabels=True, 
              yaxis_showticklabels=True, 
             title='Risk estimates correlation heatmap')
	
	fig=go.Figure(data=trace, layout=layout)
	
	return fig.show()


def plot_weights_pie_chart(weights, title, hole, hoverinfo, textinfo, textfont_size, textfont_color, marker_colors): 
	"""
	This function returns a pie chart of the optimal weights for portfolio allocation. 
	:weights (OrderedDict)
	:title (str)
	:hole (float)
	hoverinfo (str)
	textinfo (str)
	textfont_size (int)
	"""
	trace = go.Pie(labels=list(weights.keys()), values=list(weights.values()), insidetextorientation='radial')
	
	fig=go.Figure(data=trace)
	fig.update_traces(hoverinfo=hoverinfo, hole=hole, textinfo=textinfo, marker=dict(colors=marker_colors),
				  textfont_size=textfont_size, textfont_color=textfont_color)
	fig.update_layout(dict(title=title))

	return fig.show()