from flask import render_template, request
from flask.views import MethodView
from books import get_book_author

class Author(MethodView):
    def get(self):
        """
        Render the book recommend by author page.
        """
        return render_template('author.html')
    
    def post(self):
        """
        Process the form data and render the result page.
        """
        author1 = request.form.get('author1')
        author2 = request.form.get('author2')
        author3 = request.form.get('author3')
        #print(author1,author2,author3)
    
        authors = [author1, author2, author3]
        #print(authors)
    
        recommendations = get_book_author(authors)

        return render_template('results.html', author1=author1, author2=author2, author3=author3, recommendations=recommendations)