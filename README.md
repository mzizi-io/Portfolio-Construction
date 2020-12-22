## Introduction
This repository is dedicated to a progressive implementation and maintenance of various and state-to-the art techniques related to investment management decisions, portfolio construction and allocation techniques. Firstly, my interest in building these modules came from my desire to have a better risk management of the portfolio of ETFs (Trackers or Exchange-Traded Funds) that I set up to dynamise and better manage my personal savings. To do so, I did some research on the matter and finally decided to put the useful stuffs that I found here. 

The other reason is because of my ability to learn better and quicker by doing. This notebook will allow me to implement, save and test (understand backtest here) these optimization and allocation techniques. Please, be aware that I am still learning and feel free to make some constructive comments.  

## Contents
This project aims to cover the following aspects / areas: 
- Portfolio performance and risk indicators 
- Portfolio optimization techniques and methods
- Asset allocation strategies

## Features
- Portfolio performance and risk indicators which goes from *annaualized portfolio return and volatility, sharpe ratio* to *maximum drawdown, VaR, CVaR etc...*
 
- Classical portfolio optimization techniques
  - **Efficient risk portfolio**
    This is the portfolio that gives you the optimal volatility/risk exposure given a targeted return. It derives from Harry Markowitz works and findings on portfolio management theory. Also called mean_variane optimization, the idea is based on the mathematical existence of an optimal portfolio which offer the best risk-retutn couple. According to the returns of the portfolio components or assets, one can compute the optimal weights in order to build a portfolio with the best risk profile. Although, the model sounds theoretically good, there is some shortcomings such as the lack of robustness that make it less efficient in practice.
  - **Global minimum variance**
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
