from flask import Flask
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
	author = db.Column(db.Integer)
	title = db.Column(db.String)
	slug = db.Column(db.String, unique=True)
	lead = db.Column(db.String)
	body = db.Column(db.String)
	time = db.Column(db.DateTime)


@app.route('/')
def main_page():
	articles = Article.query.all()
	print(articles)
	return "<h1>Something is working</h1>"




if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
