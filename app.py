from flask import Flask, url_for, render_template, flash, request, redirect, session,logging,request
from flask_sqlalchemy import SQLAlchemy
import os
from weather import weather


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
db.create_all()
db.session.commit()

app.secret_key = os.urandom(24)


class newuser(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password

class search_history(db.Model):
	search_id= db.Column(db.Integer, primary_key=True)
	searched_city= db.Column(db.String(100))
	user_id= db.Column(db.Integer, db.ForeignKey('newuser.id'))

	def __init__(self, searched_city, user_id):
		self.searched_city = searched_city
		self.user_id=user_id
	

@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		if request.method == 'POST':

			return render_template('index.html') 
		return render_template('index.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	db.create_all()
	db.session.commit()
	if request.method == 'POST':
		new_user = newuser(username=request.form['username'], password=request.form['password'])
		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')
	return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
	
		name = request.form['username']
		passw = request.form['password']
		try:
			data = newuser.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				session['user_id'] = data.id
				return render_template('search.html')
			else:
				return 'Incorrect Login'
		# except:
		# 	return "Incorrect Login"
		except Exception as e: 
			return str(e)



@app.route("/show_weather", methods=['GET','POST'])
def show_weather():
	if request.method == 'POST':
		city=request.form['city']

	if session['logged_in'] == True:

		temperature=weather.get_weather(city)
		db.create_all()
		db.session.commit()
		new_search = search_history(searched_city=city, user_id=session['user_id'])
		db.session.add(new_search)
		db.session.commit()
		return render_template("weather.html",temperature=temperature, city=city)
	else:
		return "Please login"

@app.route("/search_data",methods=['GET','POST'])	
def search_data():
	data = search_history.query.filter_by(user_id=session['user_id']).all()
	print(type(data))
	return render_template("search_history.html",data=data)


@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))


if __name__=='__main__':
    app.run(debug=True)

