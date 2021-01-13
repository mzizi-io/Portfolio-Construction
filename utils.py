#######################################################################
# Useful functions for data processings, transformations and plotting
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


def plot_risk_estimates_heatmap(correlation_matrix, colorscale): 
	"""
	This function returns the risk estimates matrice heatmap. 
	:correlation_matrix (pd.DataFrame)
	:colorscale (str)
	"""
	correlation_matrix = pd.DataFrame(data=correlation_matrix.values, index=correlation_matrix.index.astype('str'), 
									  columns=correlation_matrix.columns)

	return correlation_matrix.iplot(kind='heatmap', colorscale=colorscale )
	
# def plot_weights_pie(): 
# 	"""
	
# 	"""
	