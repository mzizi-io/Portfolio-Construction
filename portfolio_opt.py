#################################################################################################################
#TO DO
# Allow the possibility to add some specific constraints (sector/regions/specific weights and strategies) 
# for more flexible and customizable portfolio optimization 
#################################################################################################################

import numpy as np
import pandas as pd
import scipy.stats as scp
from math import *
from collections import OrderedDict
import scipy.optimize as optimizer
from portfolio_stats import *

import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


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
            bounds=bounds, constraints=(weights_sum), options={'disp': False})
            
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
            excess_return = 1
            return - excess_return / self.portfolio_vol(weights)
            
        #Constraints
        weights_sum = ({'type':'eq', 'fun':lambda weights: np.sum(weights) - 1})
        
        weights_results = optimizer.minimize(gmv_objective_func, init_weights, method='SLSQP', 
            bounds=bounds, constraints=(weights_sum), options={'disp': False})
            
        return OrderedDict(zip(tickers, weights_results.x))


    def plot_efficient_frontier(self, portfolio_annualized_returns, risk_free_rate=0.02, num_points=30, backgroundcolor='seashell',
                                trace_linecolor='indianred', title='Efficient frontier', showlegend=True, 
                                show_max_sharpe_ratio_portfolio=None, show_global_min_variance_portfolio=None, 
                                show_equally_weighted_portfolio=None):
        """
        This function computes the optimal weights according to a list of target returns and plot the efficient frontier, the
        maximum SR portfolio, the minimum variance portfolio and the eqully-weighted portfolio.
        :portfolio_annualized_returns (pd.Series)
        :backgroundcolor (str)
        :trace_linecolor (str)
        :showlegend (bool)
        :num_points (int)
        :show_max_sharpe_ratio_portfolio (bool)
        :show_global_min_variance_portfolio (bool)
        :show_equally_weighted_portfolio (bool)
		"""
        def optimal_weights():
            """
            This internal function returns the set of optimal weights for each targeted return
            """
            set_of_optimal_weights = []
            target_returns = np.linspace(portfolio_annualized_returns.min(), portfolio_annualized_returns.max(), num_points)
            set_of_optimal_weights = [self.efficient_risk(t) for t in target_returns]		
            
            return set_of_optimal_weights
		
        # Computation of portfolio volatilities and returns based on target returns
        set_of_optimal_weights = optimal_weights()
        ef_frontier_data =pd.DataFrame(data=[[self.portfolio_return(np.asarray(list(el.values()))), self.portfolio_vol(np.asarray(list(el.values())))] 
                                             for el in set_of_optimal_weights], columns=['expected return', 'standard deviation'])
        
        # Plotting the efficient frontier
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=ef_frontier_data['standard deviation'], y=ef_frontier_data['expected return'], mode='lines+markers', 
                                 name=title, line=dict(color=trace_linecolor, width=2)))
        
        fig.update_layout(xaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)', linewidth=2),
                          yaxis=dict(showline=True, showgrid=True, linecolor='rgb(204, 204, 204)', linewidth=2), 
                          showlegend=showlegend, plot_bgcolor=backgroundcolor)
        
        # Show the maximum sharpe ratio portfolio
        if show_max_sharpe_ratio_portfolio:
            msr_weights = self.max_sharpe_ratio(risk_free_rate=risk_free_rate)
            msr_portfolio_return = pd.Series(self.portfolio_return(np.asarray(list(msr_weights.values()))))
            msr_portfolio_vol = pd.Series(self.portfolio_vol(np.asarray(list(msr_weights.values()))))
            
            fig.add_trace(go.Scatter(x=msr_portfolio_vol, y=msr_portfolio_return, mode='markers', name='Maximum Sharpe Ratio Portfolio',
                                     marker=dict(symbol='triangle-up', color='Blue', size=12)))
            

        # Show the global minimum variance portfolio
        if show_global_min_variance_portfolio:
            gmv_weights = self.global_minimum_variance()
            gmv_portfolio_return = pd.Series(self.portfolio_return(np.asarray(list(gmv_weights.values()))))
            gmv_portfolio_vol = pd.Series(self.portfolio_vol(np.asarray(list(gmv_weights.values()))))
            
            fig.add_trace(go.Scatter(x=gmv_portfolio_vol, y=gmv_portfolio_return, mode='markers', name='Global Minimum Variance Portfolio',
                                     marker=dict(symbol='triangle-up', color='DarkGreen', size=12)))

        # Show the equally-weighted portfolio
        if show_equally_weighted_portfolio:
            ew_weights = np.repeat(1/len(self.expected_returns), len(self.expected_returns))
            ew_portfolio_return = pd.Series(self.portfolio_return(ew_weights))
            ew_portfolio_vol = pd.Series(self.portfolio_vol(ew_weights))
            
            fig.add_trace(go.Scatter(x=ew_portfolio_vol, y=ew_portfolio_return, mode='markers', name='Equally-Weighted Portfolio',
                                     marker=dict(symbol='triangle-up', color='black', size=12)))
        return fig.show()

# # ----------------------------------------------------------------------------------------------------------------------------------------------# #
                       
        
                       

                       