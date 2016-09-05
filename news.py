from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

app = Flask(__name__)
app.secret_key = "something secret and unique"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2:///news"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# all queries we will ever need in one place
queries={}
queries['ARTICLES'] = "SELECT * FROM"


db = SQLAlchemy(app)

class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
	title = db.Column(db.String, nullable=False)
	slug = db.Column(db.String, unique=True, nullable=False)
	lead = db.Column(db.String)
	body = db.Column(db.String)
	time = db.Column(db.DateTime)

class Author(db.Model):
	__tablename__ = 'authors'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	bio = db.Column(db.String)
	addresses = db.relationship('Article', backref='author_detail')

class Log(db.Model):
	__tablename__ = 'log'
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String)
	ip = db.Column(postgresql.INET)
	method = db.Column(db.String)
	status = db.Column(db.String)
	time = db.Column(db.DateTime)

@app.route('/')
def main_page():
	articles = Article.query.order_by('time desc').limit(5).all()
	return render_template("articles.html", articles=articles)

@app.route('/article/new', methods=['POST', 'GET'])
def new_article():
	if request.method == 'POST':
		# title = request.form['title']
		# slug = request.form['slug']
		# lead = request.form['lead']
		# body = request.form['body']
		# print(title)
		flash("new articles not yet implemented")
		return redirect(url_for('main_page'))
	else:
		return render_template("new_article.html")

@app.route('/article/<string:slug>')
def article_page(slug):
	article = Article.query.filter(Article.slug==slug).first()
	ip = request.remote_addr
	if article:
		_log_access('/article/' + slug, ip, "200 OK", 'GET')
		return render_template("article.html", article=article)
	else:
		_log_access('/article/' + slug, ip, "404 NOT FOUND", 'GET')
		return render_template("404.html", slug=slug, ip=ip)


def _log_access(path, ip, status, method):
	log_entry = Log(path=path, ip=ip, status=status, method=method, time=datetime.now())
	db.session.add(log_entry)
	db.session.commit()

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
