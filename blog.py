#blog.py controller

from flask import Flask, render_template, request, url_for, redirect, flash, session
import sqlite3

DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)

#pulls in app config by looking for UPPERCASE variables
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid credentials.  Please try again'
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))

	return render_template('login.html', error=error)

@app.route('/main')
def main():
	return render_template('main.html')

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)