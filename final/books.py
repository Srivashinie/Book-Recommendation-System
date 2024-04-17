import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='config.env')

import requests
import openai
import random
import json
import googlemaps
from datetime import datetime
from search import search_books_by_author,search_books_by_title,search_books_by_genre

#API key of Google paces,Google books and OpenAI
gmaps = os.getenv('GOOGLEPLACES_API_KEY')
api_keyg=os.getenv('GOOGLEBOOKS_API_KEY')
openai.api_key =os.getenv('OPENAI_API_KEY')

def get_book(genres, location, authors, feeling, last_read, favorite_book, comments):
    """
    This function takes various inputs such as book genres, location, authors, feelings, last read book, favorite book, and comments.
    It retrieves information about books based on these inputs using the Google Books API and OpenAI API, and generates a list of book recommendations.

    Parameters:
        genres (str): A string representing book genres.
        location (str): A string representing the location for finding libraries and book stores.
        authors (str): A string representing the author of the books.
        feeling (str): A string representing the desired tone of the books.
        last_read (str): A string representing the last read book title.
        favorite_book (str): A string representing the favorite book title.
        comments (str): A string representing additional comments for the book recommendations.

    Returns:
        tuple: A tuple containing:
            - A list of dictionaries, each containing information about a book.
              Each dictionary includes the keys 'book' (title of the book), 'author' (author of the book),
              'cover' (URL of the book cover image), and 'link' (URL of the book information page).
            - A list of dictionaries, each containing information about a library or book store.
              Each dictionary includes the keys 'name' (name of the place) and 'address' (address of the place).
    """
    book_titles = set()
    book_authors = set()
    
    #Get library and book store loctaions
    gm = googlemaps.Client(key=gmaps)
    places = gm.places(query=f"libraries in {location}")
    libraries = []

    if places['status'] == 'OK' and len(places['results']) > 0:
        for place in places['results'][:5]:
            name = place.get('name', 'N/A')
            address = place.get('formatted_address', 'N/A')
            libraries.append({'name': name, 'address': address})
    
    places = gm.places(query=f"Book stores in {location}")

    if places['status'] == 'OK' and len(places['results']) > 0:
        for place in places['results'][:5]:
            name = place.get('name', 'N/A')
            address = place.get('formatted_address', 'N/A')
            libraries.append({'name': name, 'address': address})

    #Get books by genre
    booksgenre2 = search_books_by_genre(genres, api_keyg)
    for book in booksgenre2:
        title = book['volumeInfo']['title']
        authors = book['volumeInfo'].get('authors', [])
        if title:
            book_titles.add(title)
        if authors:
            book_authors.update(authors)

    #Get books by title
    title_books1 = search_books_by_title(last_read,api_keyg)
    for book in title_books1:
        title = book['volumeInfo']['title']
        authors = book['volumeInfo'].get('authors', [])
        if title:
            book_titles.add(title)
        if authors:
            book_authors.update(authors)

    title_books2 = search_books_by_title(favorite_book,api_keyg)
    for book in title_books2:
        title = book['volumeInfo']['title']
        authors = book['volumeInfo'].get('authors', [])
        if title:
            book_titles.add(title)
        if authors:
            book_authors.update(authors)

    #Get books by author
    author_books1 = search_books_by_author(authors, api_keyg)
    for book in author_books1:
        title = book['volumeInfo']['title']
        authors = book['volumeInfo'].get('authors', [])
        if title:
            book_titles.add(title)
        if authors:
            book_authors.update(authors)
    
    #Process the books input
    example = """
        [
         {"book": "Sense and Sensibility", "author": "Jane Austen"},
         {"book": "The Catcher in the Rye", "author": "J.D. Salinger"},
         {"book": "The Beautiful and Damned", "author": "F. Scott Fitzgerald"}
         ]
         """
    prompt = f"Generate a list of 10 book and titles based on book titles {book_titles} and authors {book_authors}.The try to match tone or mood of the book like {feeling}. Try to get books that match the comments:{comments} "
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Act as a book recomender system to help users choose what book they must read next. Use content-based filtering method to give recommendations. You will have a list of book titles and authours to make the decision. Defenitely return books that atleast match the title or author. Return json array format of books with author name and book titile like :  {'book': <book_name>, 'author': <author_name>}"},
                {"role": "user", "content": "Generate a list of 3 book and titles based on book titles {Pride and Prejudice,To Kill a Mockingbird,The Great Gatsby} and authors {J.K.Rowling,Charles Dickens,Harper Lee}."},
                {"role": "assistant", "content": example },
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
    
    resp = []
    try:
        resp = json.loads(response["choices"][0]["message"]["content"])
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    
    #Get the book Cover and link
    for book in resp:
        title = book['book']
        query = f"intitle:{title}"
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_keyg}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            if items:
                item = items[0]
                volume_info = item.get('volumeInfo', {})
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail')
                info_link = volume_info.get('infoLink')
                if thumbnail:
                    book['cover'] = thumbnail
                if info_link:
                    book['link'] = info_link

    return resp,libraries
    
#Recommend books based on the Genres    
def get_book_genre(genres):
    """
    This function takes a list of genres (`genres`) as input and retrieves information about books in those genres using the Google Books API and OpenAI API.
    It then generates a list of book recommendations based on the input genres.

    Parameters:
        genres (list): A list of strings representing book genres.

    Returns:
        list: A list of dictionaries, each containing information about a book.
        Each dictionary includes the keys 'book' (title of the book), 'author' (author of the book),
        'cover' (URL of the book cover image), and 'link' (URL of the book information page).

    """
    book_titles = set()
    book_authors = set()

    for genre in genres:
        books = search_books_by_genre(genre, api_keyg)
        for book in books:
            title = book['volumeInfo']['title']
            authors = book['volumeInfo'].get('authors', [])
            if title:
                book_titles.add(title)
            if authors:
                book_authors.update(authors)

    #Process the inputs to recommend books
    example = """
        [
         {"book": "Sense and Sensibility", "author": "Jane Austen"},
         {"book": "The Catcher in the Rye", "author": "J.D. Salinger"},
         {"book": "The Beautiful and Damned", "author": "F. Scott Fitzgerald"}
         ]
         """
    prompt = f"Generate a list of 10 book and titles based on book titles {book_titles} and authours {book_authors}. "
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Act as a book recomender system to help users choose what book they must read next. Use content-based filtering method to give recommendations. You will have a list of book titles and authours to make the decision. Return json array format of books with author name, book titile and book cover image like :  {'book': <book_name>, 'author': <author_name>}"},
                {"role": "user", "content": "Generate a list of 3 book and titles based on book titles {Pride and Prejudice,To Kill a Mockingbird,The Great Gatsby} and authors {J.K.Rowling,Charles Dickens,Harper Lee}."},
                {"role": "assistant", "content": example },
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
    
    resp = []
    try:
        resp = json.loads(response["choices"][0]["message"]["content"])
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    
    #Get the book Cover and link
    for book in resp:
        title = book['book']
        query = f"intitle:{title}"
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_keyg}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            if items:
                item = items[0]
                volume_info = item.get('volumeInfo', {})
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail')
                info_link = volume_info.get('infoLink')
                if thumbnail:
                    book['cover'] = thumbnail
                if info_link:
                    book['link'] = info_link

    return resp

#Recommend books based on the Authors  
def get_book_author(bauthors):
    """
    This function takes a list of book authors (`bauthors`) as input and retrieves information about books by those authors using the Google Books API and OpenAI API.
    It then generates a list of book recommendations based on the input authors.

    Parameters:
        bauthors (list): A list of strings representing book authors.

    Returns:
        list: A list of dictionaries, each containing information about a book.
        Each dictionary includes the keys 'book' (title of the book), 'author' (author of the book),
        'cover' (URL of the book cover image), and 'link' (URL of the book information page).
    """
    book_titles = set()
    book_authors = set()
    
    for auth in bauthors:
        books = search_books_by_author(auth, api_keyg)
        for book in books:
            title = book['volumeInfo']['title']
            authors = book['volumeInfo'].get('authors', [])
            if title:
                book_titles.add(title)
            if authors:
                book_authors.update(authors)

    #Process the input and recommend books        
    example = """
        [
         {"book": "Sense and Sensibility", "author": "Jane Austen"},
         {"book": "The Catcher in the Rye", "author": "J.D. Salinger"},
         {"book": "The Beautiful and Damned", "author": "F. Scott Fitzgerald"}
         ]
         """
    prompt = f"Generate a list of 10 book and titles based on book titles {book_titles} and authours {book_authors}. "
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Act as a book recomender system to help users choose what book they must read next. Use content-based filtering method to give recommendations. You will have a list of book titles and authours to make the decision. Return json array format of books with author name, book titile and book cover image like :  {'book': <book_name>, 'author': <author_name>}"},
                {"role": "user", "content": "Generate a list of 3 book and titles based on book titles {Pride and Prejudice,To Kill a Mockingbird,The Great Gatsby} and authors {J.K.Rowling,Charles Dickens,Harper Lee}."},
                {"role": "assistant", "content": example },
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
    
    resp = []
    try:
        resp = json.loads(response["choices"][0]["message"]["content"])
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    #print(resp)
    for book in resp:
        title = book['book']
        query = f"intitle:{title}"
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_keyg}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            if items:
                item = items[0]
                volume_info = item.get('volumeInfo', {})
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail')
                info_link = volume_info.get('infoLink')
                if thumbnail:
                    book['cover'] = thumbnail
                if info_link:
                    book['link'] = info_link

    return resp

#Recommend books based on the Titles 
def get_book_title(btitle):
    """
    This function takes a list of book titles (`btitle`) as input and retrieves information about those books using the Google Books API and OpenAI API.
    It then generates a list of book recommendations based on the input titles and authors.

    Parameters:
        btitle (list): A list of strings representing book titles.

    Returns:
        list: A list of dictionaries, each containing information about a book.
        Each dictionary includes the keys 'book' (title of the book), 'author' (author of the book),
        'cover' (URL of the book cover image), and 'link' (URL of the book information page).
    """
    book_titles = set()
    book_authors = set()
    
    for title in btitle:
        bk = search_books_by_title(title, api_keyg)
        for book in bk:
            title = book['volumeInfo']['title']
            authors = book['volumeInfo'].get('authors', [])
            if title:
                book_titles.add(title)
            if authors:
                 book_authors.update(authors)

    example = """
        [
         {"book": "Sense and Sensibility", "author": "Jane Austen"},
         {"book": "The Catcher in the Rye", "author": "J.D. Salinger"},
         {"book": "The Beautiful and Damned", "author": "F. Scott Fitzgerald"}
         ]
         """
    prompt = f"Generate a list of 10 book and titles based on book titles {book_titles} and authours {book_authors}. "
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Act as a book recomender system to help users choose what book they must read next. Use content-based filtering method to give recommendations. You will have a list of book titles and authours to make the decision. Return json array format of books with author name, book titile and book cover image like :  {'book': <book_name>, 'author': <author_name>}"},
                {"role": "user", "content": "Generate a list of 5 book and titles based on book titles {Pride and Prejudice,To Kill a Mockingbird,The Great Gatsby} and authors {J.K.Rowling,Charles Dickens,Harper Lee}."},
                {"role": "assistant", "content": example },
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
    
    resp = []
    try:
        resp = json.loads(response["choices"][0]["message"]["content"])
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    #print(resp)
    for book in resp:
        title = book['book']
        query = f"intitle:{title}"
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_keyg}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            if items:
                item = items[0]
                volume_info = item.get('volumeInfo', {})
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail')
                info_link = volume_info.get('infoLink')
                if thumbnail:
                    book['cover'] = thumbnail
                if info_link:
                    book['link'] = info_link

    return resp