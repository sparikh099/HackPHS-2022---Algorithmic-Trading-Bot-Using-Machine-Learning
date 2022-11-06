# HackPHS-2022---Algorithmic-Trading-Bot-Using-Machine-Learning
## Inspiration
Ever since middle school, I have been interested in finance and computer science. High school gave me the opportunity to intertwine both of my passions together.  At HackPHS 2022, I gained the inspiration to build my very first algorithmic trading bot. 

## What it does
This trading bot trades for me without me actually having to make a trade. To come up with an initial pool of stocks to invest in, I analyzed the top 10 stocks out of each sector to see which ones produced the most reward with the least risk. Once, I came up with a pool of stocks, I narrowed them down together so that they were optimized to their best ability. I then implemented a pairs trading algorithm that takes two pairs of stocks and hedges them. Each paired stock shares a negative to none correlation with its other stock. As one stock goes down, another stock is needed to balance out the loss, so that's how the pair works. After I did all of the research, I implemented the modeling onto QuantConnect's platform where I simulated the model on historical data(backtesting). 

## How I built it
I built it using Python 3.10.2 and Python on QuantConnect's software. I also used several of Python's libraries such as pandas, numpy, scikit-learn, statsmodels, scipy, matplotlib, and seaborn.

## Challenges I ran into
I ran into a major challenge in using the QuantConnect software. I developed my Pairs Trading Model and Reward-to-Risk Ratio asset analyzer and I needed to implement it into the backtesting software. This backtesting software tests the algorithm on historical data. QuantConnect's documentation was something that I was unfamiliar with and caused me a difficult time. I overcame this setback by reanalyzing the stack each time. 

## Accomplishments that I'm proud of
I developed a trading bot with a Sharpe Ratio of 1.683. The Sharpe Ratio is a metric that is used to measure the return on investment given the risk. The S&P 500 index's Sharpe Ratio is -0.78 and anything between 1 to 3 is said to be strong. I also implemented a Monte Carlo Simulation in my research where I analyzed the relative value at risk and relative shortfall.

## What I learned
Through this project, I was able to learn and become familiar with quant connect's software. I also learned a lot about K-means Clustering and its implementation in finance. The most important thing that I took away from this project is to constantly think like a computer if an error is present in the code. 

## What's next for Algorithmic Trading Bot using Machine Learning
The next part of this is to develop new trading bots with higher Sharpe ratios and larger expected returns. I would also like to continue expanding my knowledge of the machine learning techniques that are present in this field of quantitative finance/financial engineering. 
