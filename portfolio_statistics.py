###########################################
#TO DO
# Probabilistic Sharpe ratio 
# Deflated Sharpe ratio
###########################################

import numpy as np
import pandas as pd
import scipy.stats as scp
from math import *
        
def get_clean_data(data, components= "returns", period="monthly"): 
	"""
	This returns data depending on the type of the inputs (prices or returns) and gets the period per year 
	of the portfolio input data. It outputs the portfolio data with the right format. 
	: components_types (str) <-- {prices, returns}.
	: period (str) <-- {daily, monthly}.
	""" 
	if period == "monthly": 
		period_per_year = 12
	elif period == "daily": 
		period_per_year = 252
	else: 
		raise NotImplementedError("Expected period to be 'daily' or 'monthly'")
		
	if components == 'returns': 
		data = data
	elif components == 'prices': 
		data = data.pct_change(axis=0)
		data = data.dropna(axis=0)  
	else: 
		raise NotImplementedError("Expected components to be prices or returns data")
		
	return period_per_year, data
            
    

def annualized_volatility(returns_data, period_per_year):
    """
    This function computes the annualized volatility of the portfolio daily or monthly returns.  
    : period_per_year (int) <-- It depends on the period of the returns (e.g.: monthly or daily)
	: returns_data <-- {pd.Series or pd.DataFrame}
    """ 
    return returns_data.std() * np.sqrt(period_per_year)
    

    
    
def annualized_return(returns_data, period_per_year):
    """
    This function computes the annualized return of the portfolio daily or monthly returns.  
    : period_per_year (int) <-- It depends on the period of the returns (e.g.: monthly or daily)
	: returns_data <-- {pd.Series or pd.DataFrame}"""
    num_returns = returns_data.shape[0]
    return (1 + returns_data).prod(axis=0)** (period_per_year / num_returns) - 1




def sharpe_ratio(returns_data, period_per_year, risk_free_rate=0.04):
	"""
	Compute the sharpe ratio of portfolio indices or stocks
	: risk free rate (int) """
	rfr_per_period = (risk_free_rate + 1) ** (1 / period_per_year) - 1
	excess_return = returns_data - rfr_per_period
	num_returns = excess_return.shape[0]
	annualized_excess_return = (1 + excess_return).prod(axis=0) ** (period_per_year / num_returns) - 1
	return annualized_excess_return / (returns_data.std() * np.sqrt(period_per_year))
    

    
    
def maxDrawdown(returns_data, plot=False, style=None, legend=True, title=None, figsize=None):
	"""
	Compute drawdowns and return the maximum drawdowns of pandas series or dataframe """
	
	compound_wealth = 1000 * (1 + returns_data).cumprod(axis=0)
	prev_peaks = compound_wealth.cummax(axis=0)
	drawdowns = (compound_wealth - prev_peaks) / prev_peaks
	if plot: 
		ax = drawdowns.plot.line(style=style, legend=legend, title=title, figsize=figsize)
		return drawdowns.min(axis=0), ax
	else: 
		return drawdowns.min(axis=0)
        

		
		
def gauss_VaR(returns_data, level=5, method="gaussian"):
	"""
	Compute the gaussian value at risk or cornish-fisher VaR (parametric VaR or modified) of series of returns at predefined % level.
	method (str) <-- {gaussian, modified}
	level (int) """
        
	if method not in ["gaussian", "modified"]: 
		raise TypeError("Expected method to be 'gaussian' or 'modified'")
	if method == 'gaussian':
		#Let's compute the Z-alpha quantile 
		Z= scp.norm.ppf(level/100)
		return returns_data.mean() + Z*returns_data.std(ddof=0)
	elif method =='modified':
		#Let's compute the modified Z-alpha quantile 
		Z= scp.norm.ppf(level/100)
		s = scp.skew(returns_data)
		k = scp.kurtosis(returns_data)
		Z = (Z + (Z**2 - 1)*s/6 + (Z**3 -3*Z)*(k-3)/24 - (2*Z**3 - 5*Z)*(s**2)/36)
		return returns_data.mean() + Z*returns_data.std(ddof=0)
        
		
		
		
def historic_VaR(returns_data, level=5):
	"""
	compute the historic value at risk of series of returns at predefined % level
    level (int) """
	if isinstance(returns_data, pd.DataFrame):
		return returns_data.aggregate(compute_VaR_hist, level=level)
	elif isinstance(returns_data, pd.Series):
		return -np.percentile(returns_data, level)
	else: 
		raise NotImplementedError("Expected returns data to be Series or Dataframe)




def historic_CVaR(returns_data, level=5):
	"""
	
	"""
    if isinstance(returns_data, pd.DataFrame): 
		return returns_data.aggregate(historic_CVaR, args**)
	elif isinstance(returns_data, pd.Series):
		beyond_VaR = returns_data[returns_data<=-np.percentile(returns_data, level)]
		return beyond_VaR.mean()


								  
								  
def summary_stats():
	
	