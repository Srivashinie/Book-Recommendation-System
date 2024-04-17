import requests

def search_books_by_author(author, api_key):
    """
    Search for books by a specific author using the Google Books API.

    Parameters:
        author (str): The name of the author to search for.
        api_key (str): Google Books API key.

    Returns:
        list: A list of dictionaries, each representing a book.
              Each dictionary contains information about the book, such as title, authors, and other details.
    """
    query = f"inauthor:{author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    return []

def search_books_by_title(title, api_key):
    """
    Search for books by title using the Google Books API.

    Parameters:
        title (str): The title of the book to search for.
        api_key (str): Google Books API key.

    Returns:
        list: A list of dictionaries, each representing a book.
              Each dictionary contains information about the book, such as title, authors, and other details.
    """
    query = f"intitle:{title}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    return []

def search_books_by_genre(genre, api_key):
    """
    Search for books by genre using the Google Books API.

    Parameters:
        genre (str): The genre of the books to search for.
        api_key (str): Google Books API key.

    Returns:
        list: A list of dictionaries, each representing a book.
              Each dictionary contains information about the book, such as title, authors, and other details.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    return []
