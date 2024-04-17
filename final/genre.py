from flask import render_template, request
from flask.views import MethodView
from books import get_book_genre

class Genre(MethodView):
    def get(self):
        """
        Render the book recommendation by genre form.
        """
        return render_template('genre.html')
    
    def post(self):
        """
        Process the form data and render the result page.
        """
        genre1 = request.form.get('genre1')
        genre2 = request.form.get('genre2')
        genre3 = request.form.get('genre3')

        genres = [genre1, genre2, genre3]

        recommendations = get_book_genre(genres)

        return render_template('results.html', genre1=genre1, genre2=genre2, genre3=genre3, recommendations=recommendations)