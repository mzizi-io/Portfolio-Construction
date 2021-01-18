###########################################
#TO DO
# Probabilistic Sharpe ratio 
# Deflated Sharpe ratio
###########################################

import numpy as np
import pandas as pd
import scipy.stats as scp
from math import *
                      
def annualized_volatility(returns_data, period_per_year):
    """
    This function computes the annualized volatility of the portfolio returns.  
    :period_per_year (int) <-- It depends on the period of the returns (e.g.: monthly or daily)
	:returns_data (pd.Series or pd.DataFrame)
    """ 
    return returns_data.std() * np.sqrt(period_per_year)
    

def annualized_return(returns_data, period_per_year):
    """
    This function computes the annualized return of the portfolio returns.  
    :period_per_year (int) <-- It depends on the period of the returns (e.g.: monthly or daily)
	:returns_data (pd.Series or pd.DataFrame)
	"""
    num_returns = returns_data.shape[0]
    return (1 + returns_data).prod(axis=0)** (period_per_year / num_returns) - 1


def sharpe_ratio(returns_data, period_per_year, risk_free_rate=0.04):
	"""
	This function computes the sharpe ratio of portfolio returns.
	:period_per_year (int) <-- It depends on the period of the returns (e.g.: monthly or daily)
	:returns_data (pd.Series or pd.DataFrame)
	:risk_free_rate (int) 
	"""
	rfr_per_period = (risk_free_rate + 1) ** (1 / period_per_year) - 1
	excess_return = returns_data - rfr_per_period
	num_returns = excess_return.shape[0]
	annualized_excess_return = (1 + excess_return).prod(axis=0) ** (period_per_year / num_returns) - 1
	return annualized_excess_return / (returns_data.std() * np.sqrt(period_per_year))
    
        
def maxDrawdown(returns_data, plot=False, style=None, legend=True, title=None, figsize=None):
	"""
	This function computes the maximum drawdowns of pandas series or dataframe.
	:returns_data (pd.Series or pd.DataFrame)
	:plot (bool)
	:style (str)
	:legend (bool)
	:title (str)
	:figsize (tuple)
	"""
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
	This function computes the gaussian value at risk or cornish-fisher VaR (parametric VaR or modified) of series of returns 
	according to a predefined probability threshold level.
	:returns_data (pd.Series or pd.DataFrame)
	:method (str) <-- {gaussian, modified}
	:level (int) 
	"""     
	if method not in ["gaussian", "modified"]: 
		raise TypeError("Expected method to be 'gaussian' or 'modified'")
	if method == 'gaussian':
		#Let's compute the Z-alpha quantile 
		Z= scp.norm.ppf(level/100)
		return -(returns_data.mean() + Z*returns_data.std(ddof=0))
	elif method =='modified':
		#Let's compute the modified Z-alpha quantile 
		Z= scp.norm.ppf(level/100)
		s = scp.skew(returns_data)
		k = scp.kurtosis(returns_data)
		Z = (Z + (Z**2 - 1)*s/6 + (Z**3 -3*Z)*(k-3)/24 - (2*Z**3 - 5*Z)*(s**2)/36)
		return -(returns_data.mean() + Z*returns_data.std(ddof=0))
        
				
def historic_VaR(returns_data, level=5):
	"""
	This function computes the historical VaR (or expected shortfall) of a series of returns according to a predefined probability 
	threshold level.
	:returns_data (pd.Series or pd.DataFrame)
	:level (int)
	"""
	if isinstance(returns_data, pd.DataFrame):
		return returns_data.aggregate(historic_VaR, level=level)
	elif isinstance(returns_data, pd.Series):
		return -np.percentile(returns_data, level)
	else: 
		raise NotImplementedError("Expected 'returns data' to be Series or Dataframe")
								  
								  
def historic_CVaR(returns_data, level=5):
	"""
	This function computes the historical conditional VaR (or expected shortfall) of a series of returns according to a 
	predefined probability threshold level.
	:returns_data (pd.Series or pd.DataFrame)
	:level (int)
	"""
	if isinstance(returns_data, pd.DataFrame): 
		return returns_data.aggregate(historic_CVaR, level = level)
	elif isinstance(returns_data, pd.Series):
		beyond_VaR = returns_data[returns_data<=-np.percentile(returns_data, level)]
		return -beyond_VaR.mean()

def summary_stats(returns_data, period_per_year, risk_free_rate=0.04, VaR_method="modified", VaR_level=5): 
    """
    This function computes different statistics of portfolio returns.
    :returns_data (pd.Series or pd.DataFrame)
    :period_per_year (int) <-- It depends on the period of the returns (e.g.: monthly or daily)
    :risk_free_rate (int) 
    :VaR_method (str) <-- {gaussian, modified, historic}
    :VaR_level (int)
    """
    ann_vol = returns_data.aggregate(annualized_volatility, period_per_year = period_per_year)
    ann_return = returns_data.aggregate(annualized_return, period_per_year = period_per_year)
    sr = returns_data.aggregate(sharpe_ratio, period_per_year=period_per_year, risk_free_rate=risk_free_rate)
    
    if VaR_method not in ["gaussian", "modified", "historic"]: 
        raise NotImplementedError("Method or function has not been implemented yet")
    if VaR_method == "historic": 
        VaR = returns_data.aggregate(historic_VaR, level = VaR_level)
    else: 
        VaR = returns_data.aggregate(gauss_VaR, level = VaR_level, method = VaR_method)
    
    CVaR = returns_data.aggregate(historic_CVaR, level = VaR_level)
    maxD = maxDrawdown(returns_data, plot=False, style=None, legend=None, title=None, figsize=None)
    
    return pd.DataFrame({'Annualized return': ann_return,
                        'Annualized volatility': ann_vol,
                        'Sharpe_ratio': sr, 
                        'VaR 5%': VaR,
                        'CVaR 5%': CVaR,
                        'Max Drawdown': maxD})
             