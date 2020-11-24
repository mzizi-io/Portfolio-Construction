import numpy as np
import pandas as pd
import scipy.stats as scp
from math import *

class portfolio_statistics(object):
    """
    Compute a set of portfolio statistics
    Parameters
    -------------------------------------------------------------------------------------
    : portfolio of prices or returns (DataFrame)
    : components_types (str) <-- {prices, returns}
    : axis (int) <-- {rows:0, columns:1}
    : period (str) <-- {daily, monthly}    """

    def __init__(self, portfolio, components_types="returns", axis=0, period="monthly"):
        self.axis = axis
        self.components_types = components_types
        
        if period == "monthly": 
            self.period_per_year = 12
        elif period == "daily": 
            self.period_per_year = 252
        else: 
            raise TypeError("Exoected period to be daily or monthly")

        if self.components_types == "prices":
            portfolio = portfolio.pct_change(axis=self.axis)
            self.portfolio = portfolio.dropna(axis=self.axis)
        elif self.components_types == "returns":
            self.portfolio = portfolio
        else: 
            raise TypeError("Expected components types to be prices or returns")

    @property
    def annualized_volatility(self):
        """
        Compute the annualized volatility of the portfolio indices.   """
      
        return self.portfolio.std() * np.sqrt(self.period_per_year)

    @property
    def annualized_return(self):
        """
        Compute the annualized return of the portfolio indices or stocks """
     
        num_returns = self.portfolio.shape[0]
        return (1 + self.portfolio).prod(axis=self.axis) ** (self.period_per_year / num_returns) - 1

    def sharpe_ratio(self, rfr: int):
        """
        Compute the sharpe ratio of portfolio indices or stocks
        risk free rate (rfr) --> sharpe_ratio """
       
        rfr = rfr
        rfr_per_period = (rfr + 1) ** (1 / self.period_per_year) - 1
        excess_return = self.portfolio - rfr_per_period
        num_return = excess_return.shape[0]
        annualized_excess_return = (1 + excess_return).prod() ** (self.period_per_year / num_return) - 1

        return annualized_excess_return / self.annualized_volatility

    def maxDD(self, plot_DD=False, style=None, legend=None, figsize=None):
        """
        Compute a wealth index and drawdowns and return maxDD """
        
        compound_wealth = 1000 * (1 + self.portfolio).cumprod(axis=self.axis)
        prev_peaks = compound_wealth.cummax(axis=self.axis)
        drawdowns = (compound_wealth - prev_peaks) / prev_peaks
        if plot_DD: 
            ax = drawdowns.plot.line(style=style, legend=legend, figsize=figsize)
            return drawdowns.min(axis=self.axis), ax
        else: 
            return drawdowns.min(axis=self.axis)

    def compute_VaR(self, level=5, method="historic"):
        """
        Compute the value at risk of series of returns at predetermined level, according to different method
        method (str) <-- {historic, gaussian, modified}
        level (int) """
        
        if method not in ["historic", "gaussian", "modified"]: 
            raise TypeError("Expected method to be 'historic', 'gaussian' or 'modified'")
            
#         def historic_VaR(self, level): 
#             return -np.percentile(self.portfolio, level)
            
        if method == 'historic':
            if isinstance(self.portfolio, pd.DataFrame):
                return self.portfolio.aggregate(self.compute_VaR, level=level)
            elif isinstance(self.portfolio, pd.Series):
                return -np.percentile(self.portfolio, self.level)
        elif method == 'gaussian':
            #Let's compute the Z-alpha quantile 
            Z= scp.norm.ppf(level/100)
            return self.portfolio.mean() + Z*self.portfolio.std(ddof=0)
        elif method =='modified':
            #Let's compute the modified Z-alpha quantile 
            Z= scp.norm.ppf(level/100)
            s = scp.skew(self.portfolio)
            k = scp.kurtosis(self.portfolio)
            
            Z = (Z + (Z**2 - 1)*s/6 + (Z**3 -3*Z)*(k-3)/24 - (2*Z**3 - 5*Z)*(s**2)/36)
            return self.portfolio.mean() + Z*self.portfolio.std(ddof=0)
        
                    
#     def compute_CVaR(self, level=5, method="Historic"):
#     def summary_stats(self, ):
#         pass