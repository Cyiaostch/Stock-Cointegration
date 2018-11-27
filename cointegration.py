import os
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm as trace
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

def stationary_test(params,variables):
	result=0
	for i in range(len(params)):
		result+=params[i]*variables[i]
        
	stats=adfuller(result)
	return stats

def stationary_p(params,variables):
	result=0
	for i in range(len(params)):
		result+=params[i]*variables[i]
        
	stats=adfuller(result)
	return stats[1]

def optimize(metric,variables,learning_rate=0.01,iterations=100):
	weights=[weight for weight in np.random.random(len(variables))]
	update_history=dict()
	for i in range(len(weights)):
		update_history[i]=[]
        
	for iteration in range(iterations):
		updated_weights=[weight for weight in weights]
        
		steps=[]
		for weight in weights:
			steps.append(weight*learning_rate)
        
		for i in range(len(weights)):
			pos_step=[weight for weight in weights]
			pos_step[i]+=steps[i]
			pos_metric=metric(pos_step,variables)
            
			neg_step=[weight for weight in weights]
			neg_step[i]-=steps[i]
			neg_metric=metric(neg_step,variables)
            
			if(pos_metric<neg_metric):
				updated_weights[i]=pos_step[i]
				update_history[i].append(pos_step[i])
			else:
				updated_weights[i]=neg_step[i]
				update_history[i].append(neg_step[i])
		weights=[value for value in updated_weights]
	weights=[int(value*100) for value in weights]
	return weights, update_history

def optimize_portofolio(stocks,target,learning_rate=None,iterations=None):
	cleaned_stocks=stocks.dropna(axis=1)
	target=list(cleaned_stocks)
	portofolio=[cleaned_stocks[ticker] for ticker in target]
	best_param,update_history=optimize(stationary_p,portofolio,learning_rate,iterations)
    
	return best_param, portofolio
