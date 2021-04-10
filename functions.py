#Importing Required Libraries
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from statistics import mean, stdev
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show,output_notebook

#Importing the Data from the CSV file
stock = pd.read_csv("data/stock_usa.csv")
stock_prices = list(stock['Adj Close'])

bond = pd.read_csv("data/bond_usa.csv")
bond_prices = list(bond['Adj Close'])
date = list(bond['Date'])

stock_return = []
bond_return = []
for i in range(1, len(stock_prices)) :
    stock_return.append((stock_prices[i]-stock_prices[i-1])/stock_prices[i-1])

for i in range(1, len(bond_prices)) :
    bond_return.append((bond_prices[i]-bond_prices[i-1])/bond_prices[i-1])

no_of_year = len(stock_return)


#Calculating Mean of the Data
stock_mean = mean(stock_return)
bond_mean = mean(bond_return)

#Calculating Variance of the Stock
stock_var = 0
for i in stock_return :
    stock_var += (i-stock_mean)**2
stock_var /= no_of_year

#Calculating Variance of the Bond
bond_var = 0
for i in bond_return :
    bond_var += (i-bond_mean)**2
bond_var /= no_of_year

#Calculating Standard Deviation of the Data
stock_sd = stdev(stock_return)
bond_sd = stdev(bond_return)

#Calculating Risk Premium
risk_free_return = 0.0019 #Risk free return(19% for American Market and 5.64% for Indian Market)
stock_rp = (stock_mean - risk_free_return)  #Risk Premium
bond_rp = (bond_mean - risk_free_return)  #Risk Premium

#Calculating Correlation
correl = 0
mean_deviation = 0
stock_mean_deviation_square = 0
bond_mean_deviation_square = 0
for i in range(no_of_year) :
    mean_deviation += (stock_return[i]-stock_mean)*(bond_return[i]-bond_mean)
    stock_mean_deviation_square += (stock_return[i]-stock_mean)**2
    bond_mean_deviation_square += (bond_return[i]-bond_mean)**2
correl = mean_deviation/sqrt((stock_mean_deviation_square*bond_mean_deviation_square))

#Calculating Covariance
covar = mean_deviation/no_of_year

#Rounding Values
stock_mean = round(stock_mean, 3)
bond_mean = round(bond_mean, 3)
stock_var = round(stock_var, 5)
bond_var = round(bond_var, 5)
stock_sd = round(stock_sd, 3)
bond_sd = round(bond_sd, 3)
stock_rp = round(stock_rp, 3)
bond_rp = round(bond_rp, 3)

#Constructing different Portfolios
stock_percentage = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
bond_percentage = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0]
portfolio_mean = []
portfolio_var = []
portfolio_std = []
portfolio_rp = []
for i in range(len(stock_percentage)) :
    portfolio_mean.append((stock_percentage[i]*stock_mean)+(bond_percentage[i]*bond_mean))
    portfolio_var.append(((stock_percentage[i]**2)*stock_var)+((bond_percentage[i]**2)*bond_var))
    portfolio_std.append(sqrt(portfolio_var[i]))
    portfolio_rp.append(portfolio_mean[i]-risk_free_return)
    portfolio_mean[i] = round(portfolio_mean[i], 5)*100
    portfolio_std[i] = round(portfolio_std[i], 5)*100
    portfolio_var[i] = round(portfolio_var[i], 5)*100

################## Results ################################

#Outputting Different Portfolio
Porfolio = pd.DataFrame(
    {'Stock': stock_percentage,
     'Bond': bond_percentage,
     'Mean': portfolio_mean,
     'Variance' : portfolio_var,
     'Std. Deviation' : portfolio_std
    })
lowest_risk = portfolio_std.index(min(portfolio_std))
print(Porfolio)
print("The Portfolio having minimum risk and highest return as compared to others is : %d stocks and %d bonds" %(stock_percentage[lowest_risk]*100, bond_percentage[lowest_risk]*100))


#Plotting the Markowitz Bullet Graph
TOOLS = [BoxSelectTool(), HoverTool()]
p = figure(plot_width = 400, plot_height = 400, tools=TOOLS)
p.xaxis.axis_label = "Risk"
p.yaxis.axis_label = "Return"
p.circle(portfolio_std, portfolio_mean, 
         size = 10, color = "navy", alpha = 0.5)
show(p)
# plt.scatter(portfolio_std, portfolio_mean)
# plt.xlabel("Risk")
# plt.ylabel("Return")
# plt.title("Two Assets Portfolio Optimization")
# plt.show()