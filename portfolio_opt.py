import numpy as np
import pandas as pd
import scipy.stats as scp
from math import *
from collections import OrderedDict
import scipy.optimize as optimizer
from portfolio_statistics import portfolio_statistics as ps


class mean_variance_opt(object): 
    """
    Mean-variance optimization class with the following public methods: 
        - portfolio_vol
        - portfolio_return
        - efficient_risk
        - minimum_var
        - max_sharpe_ratio
        - equally_weighted
    
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
        weights --> This function computes the volatility of the portfolio.
        """
        return (weights.T @ self.risk_estimates @ weights)**0.5
    
    
	
	
    def portfolio_return(self, weights): 
        """
        weights --> This function computes the expected return of the portfolio.
        """
        return weights.T @ self.expected_returns    

    
	
	
    def efficient_risk(self, target_return):
        """
        target_return --> This function computes the optimal portfolio weights to get the efficient risk portfolio 
                          with the miminum volatility that one can get, based on a targeted return.
        """     
        tickers = self.expected_returns.index
        n_tickers = len(self.expected_returns)
        init_weights = np.repeat(1/n_tickers, n_tickers)
        bounds = ((0.0,1.0),)*n_tickers
        
        #Set up the constraints
        weights_sum = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        return_is_reached = ({'type': 'eq', 'fun': lambda weights: self.portfolio_return(weights) - target_return})

        weights = optimizer.minimize(self.portfolio_vol, init_weights, method='SLSQP', bounds=bounds,
                           constraints = (weights_sum, return_is_reached), options={'disp': False})
                       
        return OrderedDict(zip(tickers, weights.x))
    
    
	
	
    def max_sharpe_ratio(self, risk_free_rate=0.04): 
        """
        
        """
        def objective_func(): 
            """
            Negative sharpe ratio
            """       
            excess_return = self.portfolio_return(weights) - risk_free_rate
            annualized_excess_return = 
            annualized_vol =
            return - annualized_excess_return / annualized_vol
            

       
    def minimum_var(self, ): 
        """
        
        """
        pass

    #************************************************************************************************************* 
    def equally_weighted(): 
        pass
                       
                       
# class custom_optimizer(object):
#       def add_constraints(self): 
#                        pass
                       
        
                       

                       