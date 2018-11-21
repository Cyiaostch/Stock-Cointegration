import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import fix_yahoo_finance
import pandas_datareader.data as web
import urllib3
import matplotlib.style as style
import random
import bs4 as bs
import pickle
import requests
import os
import json
import quandl
from pandas_datareader._utils import RemoteDataError


def get_tickers():
#Get tickers of IHSG stocks
#Return list
	resp = requests.get('https://id.wikipedia.org/wiki/Daftar_perusahaan_yang_tercatat_di_Bursa_Efek_Indonesia')
	soup = bs.BeautifulSoup(resp.text,'html.parser')
	tables = soup.findAll('table', {'class': 'wikitable sortable'})
	tickers=[]
	for table in tables:
		for row in table.findAll('tr')[1:]:
			ticker = row.findAll('td')[0].text
			tickers.append(ticker[5:])
	tickers.sort()
	return tickers[1:]
    
def get_data(tickers,start_date,end_date):
#Download IHSG stocks data from google finance
#Returns Pandas Dataframe
#Data are pandas.DataFrame object    
#Data are saved in form of .csv file
	start = start_date
	end = end_date
	stocks_data={}
	for ticker in tickers:
		success=True
		try:
			df = web.get_data_yahoo('{}.JK'.format(ticker), start, end)
		except RemoteDataError:
			success=False
		if(success):    
			stocks_data[ticker]=df
	return stocks_data
	
def compile_data(stocks,col_label,tickers):
#Combine all one specified columns of IHSG stocks data
#Return pandas.DataFrame object
	compiled=pd.DataFrame()
	for count,ticker in enumerate(tickers):
		stock=stocks[ticker]
		stock.set_index('Date',inplace=True)
		col=list(stock)
		col.remove(col_label)
		stock.rename(columns={col_label:ticker},inplace=True)
		stock.drop(col,1,inplace=True)
		if compiled.empty:
			compiled=stock
		else:
			compiled=compiled.join(stock,how='outer')
	return(compiled)

