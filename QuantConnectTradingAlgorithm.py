#Shyam Parikh
#November 5, 2022
#Hack PHS Code

import numpy as np
import pandas as pd
from scipy import stats
from math import floor
from datetime import timedelta
from collections import deque
import itertools as it
from decimal import Decimal
# endregion

class GeekyGreenElephant(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        #Adds these tickers to the collection of stocks
        self.AddEquity("LLY", Resolution.Daily)
        self.AddEquity("COP", Resolution.Daily)
        self.AddEquity("ENGH", Resolution.Daily)
        self.AddEquity("MPC",Resolution.Daily)
        self.AddEquity("ANET", Resolution.Daily)
        ##Adds the following tickers to the hedging pairs
        tickers = ['ABT', 'ACN','AAL', 'AIG', 'AKAM','ALLE', 'AVGO', 'BAX', 'CPT', 'CTSH', 'EMR', 'ESS', 'FRT','HPE', 'IPG','JNPR', 'KIM', 'LUV', 'MA', 'MKC', 'NLOK', 'NXPI',  'PG', 'PRU', 'REG', 'ROP','TECH', 'TRMB','AAP', 'USB', 'APH', 'BMY','DRI','NDSN','A', 'RMD', 'BIO',  'CHTR', 'LRCX', 'NTRS',  'PEAK',  'TER', 'ADBE', 'VFC', 'FCX', 'MAR','TGT', 'ALB', 'ALGN', 'CZR', 'ILMN', 'SBNY',]
        self.threshold = 2
        self.symbols = []
        ##Appends the tickers to the list of stock symbols
        for i in tickers:
            self.symbols.append(self.AddEquity(i, Resolution.Daily).Symbol)
        self.formation_period = 252
        self.history_price = {}
        for symbol in self.symbols:
            hist = self.History([symbol], self.formation_period+1, Resolution.Daily)
            if hist.empty: 
                self.symbols.remove(symbol)
            else:
                self.history_price[str(symbol)] = deque(maxlen=self.formation_period)
                for tuple in hist.loc[str(symbol)].itertuples():
                    self.history_price[str(symbol)].append(float(tuple.close))
                if len(self.history_price[str(symbol)]) < self.formation_period:
                    self.symbols.remove(symbol)
                    self.history_price.pop(str(symbol))
        self.sorted_pairs = list((('AAL', 'FCX'), ('AAL', 'MAR'), ('AAL', 'TGT'), ('ALGN', 'CZR'), ('ALGN', 'ILMN'), ('ALGN', 'SBNY'), ('AAP', 'IPG'), ('AAP', 'JNPR'), ('AAP', 'KIM'), ('AAP', 'LUV'), ('AAP', 'MA'), ('AAP', 'MKC'), ('AAP', 'NLOK'), ('AAP', 'NXPI'), ('AAP', 'PG'), ('AAP', 'PRU'), ('AAP', 'REG'), ('AAP', 'ROP'), ('AAP', 'TECH'), ('AAP', 'TRMB'), ('AAP', 'USB'), ('A', 'APH'), ('A', 'BMY'), ('A', 'DRI'), ('A', 'NDSN'), ('A', 'RMD'), ('ADBE', 'BIO')))  
        self.count = 0
    #Method that executes the Trades
    def OnData(self, data: Slice):
        if not self.Portfolio.Invested:
            #Safety Net of Stocks
            self.SetHoldings("LLY", 0.37457 * 0.5)
            self.SetHoldings("COP", 0.31107  * 0.5)
            self.SetHoldings("ENGH", 0.20413 * 0.5)
            self.SetHoldings("MPC", 0.08817 * 0.5)
            self.SetHoldings("ANET", 0.2205 * 0.5)  
        for i in self.sorted_pairs:
            # calculate the spread of two price series
            spread = np.array(self.history_price[str(i[0])]) - np.array(self.history_price[str(i[1])])
            mean = np.mean(spread)
            std = np.std(spread)
            ratio = self.Portfolio[i[0]].Price / self.Portfolio[i[1]].Price
            # long-short position is opened when pair prices have diverged by two standard deviations
            if spread[-1] > mean + self.threshold * std:
                if not self.Portfolio[i[0]].Invested and not self.Portfolio[i[1]].Invested:
                    quantity = int(self.CalculateOrderQuantity(i[0], 0.2))
                    self.Sell(i[0], quantity) 
                    self.Buy(i[1],  floor(ratio*quantity))                
            
            elif spread[-1] < mean - self.threshold * std: 
                quantity = int(self.CalculateOrderQuantity(i[0], 0.2))
                if not self.Portfolio[i[0]].Invested and not self.Portfolio[i[1]].Invested:
                    self.Sell(i[1], quantity) 
                    self.Buy(i[0], floor(ratio*quantity))  
                    
            # the position is closed when prices revert back
            elif self.Portfolio[i[0]].Invested and self.Portfolio[i[1]].Invested:
                    self.Liquidate(i[0]) 
                    self.Liquidate(i[1])     
    
    def Rebalance(self):
        # schedule the event to fire every half year to select pairs with the smallest historical distance
        if self.count % 6 == 0:
            distances = {}
            for i in self.symbol_pairs:
                distances[i] = Pair(i[0], i[1], self.history_price[str(i[0])],  self.history_price[str(i[1])]).distance()
                self.sorted_pairs = sorted(distances, key = lambda x: distances[x])[:4]
        self.count += 1


#Creates the Hedge Pair Object
class Pair:
    def __init__(self, symbol_a, symbol_b, price_a, price_b):
        self.symbol_a = symbol_a
        self.symbol_b = symbol_b
        self.price_a = price_a
        self.price_b = price_b
    
    def distance(self):
        # calculate the sum of squared deviations between two normalized price series
        norm_a = np.array(self.price_a)/self.price_a[0]
        norm_b = np.array(self.price_b)/self.price_b[0]
        return sum((norm_a - norm_b)**2)