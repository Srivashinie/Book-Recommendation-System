import flask
import os
from dotenv import load_dotenv
from flask_cors import CORS

from index import Index
from recommend import Recommend
from genre import Genre
from author import Author
from title import Title

load_dotenv(dotenv_path='config.env')
app = flask.Flask(__name__) 
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# this is to redirect to home page
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET","POST"])

# this is to redirect to recommend page
app.add_url_rule('/recommend',
                 view_func=Recommend.as_view('recommend'),
                 methods=["GET","POST"])

# this is to redirect to recommend by genre page
app.add_url_rule('/genre',
                 view_func=Genre.as_view('genre'),
                 methods=["GET","POST"])

# this is to redirect to recommend by genre page
app.add_url_rule('/author',
                 view_func=Author.as_view('author'),
                 methods=["GET","POST"])

# this is to redirect to recommend by title page
app.add_url_rule('/title',
                 view_func=Title.as_view('title'),
                 methods=["GET","POST"])

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
