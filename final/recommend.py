from flask import render_template, request
from flask.views import MethodView
from books import get_book

class Recommend(MethodView):
    def get(self):
        """
        Render the book recommendation form.
        """
        return render_template('recommend.html')

    def post(self):
        """
        Process the form data and render the result page.
        """
        genres = request.form.get('genres')
        location = request.form.get('location')
        authors = request.form.get('authors')
        feeling = request.form.get('feeling')
        last_read = request.form.get('last_read')
        favorite_book = request.form.get('favorite_book')
        comments = request.form.get('comments')

        recommendations,libraries = get_book(genres, location, authors, feeling, last_read, favorite_book, comments)
     
        return render_template('results.html', genres=genres, location=location, authors=authors, feeling=feeling, last_read=last_read, favorite_book=favorite_book, comments=comments, recommendations=recommendations,libraries=libraries)
