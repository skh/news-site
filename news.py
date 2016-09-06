#!/usr/bin/env python3

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy import desc

app = Flask(__name__)
app.secret_key = "something secret and unique"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2:///news"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
	articles = Article.query.order_by(desc(Article.time)).limit(5).all()
	return render_template("articles.html", articles=articles)

@app.route('/article/new', methods=['POST', 'GET'])
def new_article():
	if request.method == 'POST':
		title = request.form.get('title')
		slug = request.form.get('slug')
		lead = request.form.get('lead')
		body = request.form.get('body')

		if (not title or not slug or not lead or not body):
			flash("Please fill in all fields.")
			return render_template("new_article.html",
									title=title, slug=slug,
									lead=lead, body=body)
		else:
			slug_in_use = Article.query.filter(Article.slug==slug).count()
			if slug_in_use:
				flash("The slug %s is already in use. Please choose another one." % (slug))
				return render_template("new_article.html", title=title,
										lead=lead, body=body)
			else:
				article = Article(title=title, slug=slug,
									 lead=lead, body=body,
									 time=datetime.now(), author=3)	# Anonymous Contributor
				db.session.add(article)
				db.session.commit()
				flash("Article successfully created.")
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
