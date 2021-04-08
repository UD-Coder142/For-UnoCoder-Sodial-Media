from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(20000), nullable=False)
	sender = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return "<Name %r>" % self.id

global session
session = {}
session['logged_in'] = False
session['username'] = ''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if not session['logged_in']:
		if request.method == 'POST':
			value = str(request.form.get('input'))
			session['username'] = value
			session['logged_in'] = True

			return redirect(url_for('profile', user=value))
		else:
			return render_template('index.html')
	else:
		return redirect(url_for('profile', user=session['username']))

@app.route('/actions/post', methods=['GET', 'POST'])
def post():
	if session['logged_in']:
		if request.method == 'POST':
			value = str(request.form.get('input'))
			message = Messages(content=value, sender=session['username'])

			db.session.add(message)
			db.session.commit()

			return redirect(url_for('posts'))
		else:
			return render_template('post.html')
	else:
		return redirect(url_for('login'))

@app.route('/actions/posts', methods=['GET', 'POST'])
def posts():
	messages = Messages.query.order_by(Messages.date_created)
	return render_template('posts.html', posts=messages, user=session['username'])

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if session['logged_in']:
		session['logged_in'] = False
		return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

@app.route('/users/<user>', methods=['GET', 'POST'])
def profile(user):
	if session['logged_in']:
		return render_template('profile.html', name=user)
	else:
		return redirect(url_for('login'))

@app.route('/')
def index():
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)