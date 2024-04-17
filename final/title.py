from flask import render_template, request
from flask.views import MethodView
from books import get_book_title

class Title(MethodView):
    def get(self):
        """
        Render the book recommendation by title form.
        """
        return render_template('title.html')
    
    def post(self):
        """
        Process the form data and render the result page.
        """
        book1 = request.form.get('book1')
        book2 = request.form.get('book2')
        book3 = request.form.get('book3')

        books = [book1, book2, book3]

        recommendations = get_book_title(books)

        return render_template('results.html', book1=book1, book2=book2, book3=book3, recommendations=recommendations)
