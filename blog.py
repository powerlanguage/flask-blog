#blog.py controller

from flask import Flask, render_template, request, url_for, redirect, flash, session, g
from functools import wraps #used for wrapping functions in other functions like decorators
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

#login checking decorator
#if 'logged_in' is in session call the function that is wrapped
#otherwise display the error and redirect to login
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first!')
			return redirect(url_for('login'))
	return wrap

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
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('SELECT * FROM posts')
	#returns a list of dicts?
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields required, plz try again")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('INSERT INTO posts (title, post) values (?,?)', (title, post))
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))

if __name__ == '__main__':
	app.run(debug=True)