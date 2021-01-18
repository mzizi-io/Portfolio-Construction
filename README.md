## Introduction
Here is a link of a cookbook which tests and shows how to use the python functions and modules which are curently implemented : 
\href{https://nbviewer.jupyter.org/github/Olaymka/Portfolio-Construction/blob/main/cookbook.ipynb#}

This repository is dedicated to the progressive implementation and maintenance of various and state-to-the art techniques related to investment management decisions, portfolio construction and allocation techniques. First of all, my interest in building these modules came from my desire to have a better risk management of the portfolio of ETFs (Trackers or Exchange-Traded Funds) that I set up to boost and better manage my personal savings. To do so, I did some research on the matter and finally decided to put here the useful elements that I found. 

The other reason is my ability to learn better and faster through practice. This notebook will allow me to implement, save and test (understand backtest here) these optimization and allocation techniques. 

Please, know that I am still learning and do not hesitate to make constructive comments.  

## Contents
This project aims to cover the following aspects / areas: 
- Portfolio performance and risk indicators 
- Portfolio optimization techniques and methods
- Asset allocation strategies

## Features
- Portfolio performance and risk indicators which goes from *annaualized portfolio return and volatility, sharpe ratio* to *maximum drawdown, VaR, CVaR etc...*
 
- Classical portfolio optimization techniques: 
  - **Efficient risk portfolio:**
    This is the portfolio that gives you the optimal volatility/risk exposure given a targeted return. It comes from Harry Markowitz works and findings on the theory of portfolio management. Also known as mean-variance optimization, the idea is based on the mathematical existence of an optimal portfolio that offers the best risk/return trade-off. Based on the returns of the portfolio components or assets, optimal weightings can be calculated in order to build a portfolio with the best risk profile. Although the model looks good in theory, it has some shortcomings, such as its lack of robustness, which make it less effective in practice.
    
  - **Global minimum variance:**
    This is the portfolio that offers the lower possible return's variance. 
  - **Maximum sharpe ratio portfolio**
  - **Equally-weighted portfolio**
 
## To do / Improvement
This project is ongoing and there is still a lot to do in order to cover all aspects of portfolio management. Hereafter, some ideas / techniques and methods I will implement very soon: 
- Risk estimates techniques (covariance estimates)
- Expected returns estimates techniques
- Allocation strategies and techniques (CPPI, LDI...)
- Custom portfolio optimization

## Disclaimer 
Nothing about this project constitues an investment advice. The author bears no responsibiltiy for your subsequent investment decisions.
