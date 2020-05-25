from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps
import cointegration
import data_fetching
import pprint

app = Flask(__name__)

app.config['SECRET_KEY'] = ''

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token') 
		if not token:
			return jsonify({'message' : 'Token is missing!'}), 403

		try: 
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'message' : 'Token is invalid!'}), 403

		return f(*args, **kwargs)

	return decorated

@app.route('/login/<username>/<password>/')
def login(username,password):
	if username=="" and password=='':
		token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'])

		return jsonify({'token':token.decode('UTF-8')})

	return jsonify({'token':"INVALID"})

@app.route('/getResult/<tickers>/<start_date>/<end_date>/')
@token_required
def getResult(tickers,start_date,end_date):
	tickers=tickers.split(",")
	start_date=start_date
	end_date=end_date
	response_parameters=generate_response(tickers,start_date,end_date)
	return jsonify(
		tickers=tickers,
		best_parameters=response_parameters[0],
		test_statistics=response_parameters[2],
		p_value=response_parameters[3],
		critical_value_1=response_parameters[4],
		critical_value_5=response_parameters[5],
		critical_value_10=response_parameters[6])

def generate_response(tickers,start_date,end_date):
	stocks_data=data_fetching.get_data(tickers,start_date,end_date)
	compiled_stocks_data=data_fetching.compile_data(stocks_data,"Close",tickers)
	optimized_portofolio=cointegration.optimize_portofolio(compiled_stocks_data,tickers,0.01,100)
	best_parameters,portofolio=optimized_portofolio
    

	dicky_fuller_statistics=cointegration.stationary_test(best_parameters,portofolio)
	test_statistics=dicky_fuller_statistics[0]
	p_value=dicky_fuller_statistics[1]
	critical_value_1=dicky_fuller_statistics[4]['1%']
	critical_value_5=dicky_fuller_statistics[4]['5%']
	critical_value_10=dicky_fuller_statistics[4]['10%']
    
	return best_parameters,portofolio,test_statistics,p_value,critical_value_1,critical_value_5,critical_value_10

if __name__ == '__main__':
	app.run(debug=True)
