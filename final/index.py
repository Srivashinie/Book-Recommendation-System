from flask import render_template, request
from flask.views import MethodView
from books import get_book

class Index(MethodView):
    def get(self):
        """
        Render the book index page.
        """
        return render_template('index.html')
