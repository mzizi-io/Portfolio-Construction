import numpy as np
import pandas as pd
import scipy.stats as scp
from math import *
from collections import OrderedDict
import scipy.optimize as optimizer
from portfolio_stats import *


class mean_variance_opt(object): 
    """
    Mean-variance optimization class with the following public methods: 
        - portfolio_vol
        - portfolio_return
        - efficient_risk
        - global minimum variance portfolio
        - max_sharpe_ratio portfolio

    """
    def __init__(self, expected_returns, risk_estimates): 
        """
        Constructor of the mean-variance optimization class with expected returns and covariance matrice.
        Expected returns have to be annualized returns in order to get accurates optimal components weights. 
        """
        self.expected_returns = expected_returns
        self.risk_estimates = risk_estimates
        
		
    def portfolio_vol(self, weights): 
        """
        :weights (float) --> This function computes the volatility of the portfolio.
        """
        return (weights.T @ self.risk_estimates @ weights)**0.5
    
    
    def portfolio_return(self, weights): 
        """
        :weights (float) --> This function computes the expected return of the portfolio.
        """
        return weights.T @ self.expected_returns    

    
    def efficient_risk(self, target_return):
        """
        :target_return (float) --> This function computes the optimal portfolio weights to get the efficient risk portfolio 
                          with the miminum volatility that one can get, based on a targeted return.
        """     
        tickers = self.expected_returns.index
        n_tickers = len(self.expected_returns)
        init_weights = np.repeat(1/n_tickers, n_tickers)
        bounds = ((0.0,1.0),)*n_tickers
        
        #Set up the constraints
        weights_sum = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        return_is_reached = ({'type': 'eq', 'fun': lambda weights: self.portfolio_return(weights) - target_return})

        weights_results = optimizer.minimize(self.portfolio_vol, init_weights, method='SLSQP', bounds=bounds,
                           constraints = (weights_sum, return_is_reached), options={'disp': False})
                       
        return OrderedDict(zip(tickers, weights_results.x))
    
    
    def max_sharpe_ratio(self, risk_free_rate=0.04): 
        """
        :risk_free_rate (float) --> Maximum Sharpe Portfolio or Tangency Portfolio is a portfolio that maximizes
                                    the risk-adjusted return. It is the point where line drawn from the point (0, risk-free rate)
                                    is tangent to the efficient frontier.
        """
        def msr_objective_func(weights, risk_free_rate=0.04): 
            """
            The objective function here is the negative sharpe ratio. We get the optimal weights to determine the max sharpe ratio
            by mimizing the negative sharpe ratio objective function.
            """       
            excess_return = self.portfolio_return(weights) - risk_free_rate
            return - excess_return / self.portfolio_vol(weights)
            
        tickers = self.expected_returns.index
        n_tickers = len(self.expected_returns)
        init_weights = np.repeat(1/n_tickers, n_tickers)
        bounds = ((0.0,1.0),)*n_tickers
        
        #Constraints
        weights_sum = ({'type':'eq', 'fun':lambda weights: np.sum(weights) - 1})
        
        weights_results = optimizer.minimize(msr_objective_func, init_weights, (risk_free_rate,), method='SLSQP', 
            bounds = bounds, constraints=(weights_sum), options={'disp': False})
            
        return OrderedDict(zip(tickers, weights_results.x))
            

    def global_minimum_variance(self): 
        """
        The aim is to make the objective function being insensitive to expected returns. Then, we will have one degree of liberty which is the
        portfolio volatility that we want to minimize.
        """
        tickers = self.expected_returns.index
        n_tickers = len(self.expected_returns)
        init_weights = np.repeat(1/n_tickers, n_tickers)
        bounds = ((0.0,1.0),)*n_tickers
        
        def gmv_objective_func(weights): 
            """
            The objective function here is a modified negative sharpe ratio. we set up contant and fixed excess return and minimize the 
            negative sharpe ratio in order to get the optimal weights to compute the global minimum variance portfolio.
            """       
            excess_return = np.repeat(1, n_tickers)
            return - excess_return / self.portfolio_vol(weights)
            
        #Constraints
        weights_sum = ({'type':'eq', 'fun':lambda weights: np.sum(weights) - 1})
        
        weights_results = optimizer.minimize(msr_objective_func, init_weights, (risk_free_rate,), method='SLSQP', 
            bounds = bounds, constraints=(weights_sum), options={'disp': False})
            
        return OrderedDict(zip(tickers, weights_results.x))


# 		def plot_efficient_frontier(self, num_points=20, show_max_sharpe_ratio_portfolio=None, show_global_min_variance_portfolio=None, show_equally_weighted_portfolio=None): 
# #         """
        
# #         """
# #         def optimal_weights(num_target_returns): 
# #             """
            
# #             """
            
            
# #             target_returns = np.linspace(portfolio_annualized_returns.min, portfolio_annualized_returns.min, num_points)
            
            
                       
# # class custom_optimizer(object):
# #       def add_constraints(self): 
# #                        pass
                       
        
                       

                       