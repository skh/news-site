from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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



@app.route('/')
def main_page():
	articles = Article.query.order_by('time desc').limit(5).all()
	return render_template("articles.html", articles=articles)

@app.route('/article/<string:slug>')
def article_page(slug):
	article = Article.query.filter(Article.slug==slug).first()
	if article:
		return render_template("article.html", article=article)
	else:
		return render_template("404.html", slug=slug)

def _log_success():
	pass

def log_error():
	pass



if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
