import requests
from django.core.management.base import BaseCommand
from project.models import Author, Book
from dateutil import parser
import re



class Command(BaseCommand):
    help = "Load books and authors from Google Books API and Open Library API into the database"

    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
    OPEN_LIBRARY_AUTHOR_SEARCH_URL = "https://openlibrary.org/search/authors.json"
    OPEN_LIBRARY_AUTHOR_DETAILS_URL = "https://openlibrary.org/authors/{}.json"
    GOOGLE_API_KEY = "AIzaSyDlKkk-tLl71yvjuolcGBnbpdfCO7JI_po"  # Replace with your Google Books API key

    def fetch_books_from_google(self, query, start_index=0, max_results=40):
        """
        Fetch books from Google Books API using a query.
        """
        params = {
            "q": query,
            "startIndex": start_index,
            "maxResults": max_results,
            "key": self.GOOGLE_API_KEY,
        }
        response = requests.get(self.GOOGLE_BOOKS_API_URL, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            self.stdout.write(f"Failed to fetch books from Google Books API: {response.status_code}")
            return []

    def fetch_author_details_from_open_library(self, author_name):
        """
        Fetch detailed author information from Open Library API.
        """
        search_params = {"q": author_name}
        response = requests.get(self.OPEN_LIBRARY_AUTHOR_SEARCH_URL, params=search_params)
        if response.status_code == 200:
            results = response.json().get("docs", [])
            if results:
                # Get the first matched author
                author_data = results[0]
                author_key = author_data.get("key")
                detail_response = requests.get(self.OPEN_LIBRARY_AUTHOR_DETAILS_URL.format(author_key))
                if detail_response.status_code == 200:
                    return detail_response.json()
        return None

    def save_author(self, author_name, google_author_id=None):
        """
        Save an author to the database, enriching details from Open Library API.
        """
        # Split the author's name into first and last names
        name_parts = author_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Fetch additional details from Open Library
        author_details = self.fetch_author_details_from_open_library(author_name)
        biography = None
        birth_date = None
        death_date = None

        if author_details:
            biography = author_details.get("bio", None)
            if isinstance(biography, dict):  # Handle Open Library bio format
                biography = biography.get("value", "")

            birth_date = self.parse_date_author(author_details.get("birth_date", None))
            death_date = self.parse_date_author(author_details.get("death_date", None))

        # Save or retrieve the author
        author, created = Author.objects.get_or_create(
            author_first_name=first_name,
            author_last_name=last_name,
            defaults={
                "author_google_id": google_author_id,
                "author_biography": biography,
                "author_birth_date": birth_date,
                "author_death_date": death_date,
            },
        )
        if created:
            self.stdout.write(f"Saved author: {author}")
        return author

    def parse_date_author(self, date_str):
        """
        Parse a date string into a date object. Returns None if parsing fails.
        """
        if not date_str:
            return None

        try:
            # Try parsing using dateutil.parser
            parsed_date = parser.parse(date_str, fuzzy=True)
            return parsed_date.date()
        except (ValueError, TypeError):
            # Handle special cases or localized dates
            # Example: Convert "3 maggio 1985" to "3 May 1985"
            localized_months = {
                "gennaio": "January", "febbraio": "February", "marzo": "March",
                "aprile": "April", "maggio": "May", "giugno": "June",
                "luglio": "July", "agosto": "August", "settembre": "September",
                "ottobre": "October", "novembre": "November", "dicembre": "December",
            }
            for italian, english in localized_months.items():
                date_str = re.sub(rf"\b{italian}\b", english, date_str, flags=re.IGNORECASE)

            try:
                # Try parsing again after replacing localized months
                parsed_date = parser.parse(date_str, fuzzy=True)
                return parsed_date.date()
            except (ValueError, TypeError):
                # Log or print the invalid date for debugging
                print(f"Invalid date format: {date_str}")
                return None

    def save_book(self, book_data):
        """
        Save a book to the database, avoiding duplicates.
        """
        # Extract book details
        volume_info = book_data.get("volumeInfo", {})
        book_google_id = book_data.get("id", "Untitled")
        book_title = volume_info.get("title", "Untitled")
        book_subtitle = volume_info.get("subtitle", "")
        book_categories = ', '.join(volume_info.get("categories", []))
        book_description = volume_info.get("description", "")
        book_publish_date = self.parse_date(volume_info.get("publishedDate", ""))
        book_cover_image = volume_info.get("imageLinks", {}).get("thumbnail", None)
        book_page_count = volume_info.get("pageCount", None)
        book_languages = volume_info.get("language", "")

        # Handle the first author only
        authors = volume_info.get("authors", [])
        if authors:
            author_name = authors[0]
            author = self.save_author(author_name, google_author_id=book_google_id)
        else:
            self.stdout.write(f"No author found for book: {book_title}")
            return

        # Save or retrieve the book
        book, created = Book.objects.get_or_create(
            book_google_id=book_google_id,
            book_author=author,
            defaults={
                "book_title": book_title,
                "book_subtitle": book_subtitle,
                "book_categories": book_categories,
                "book_description": book_description,
                "book_publish_date": book_publish_date,
                "book_cover_image": book_cover_image,
                "book_page_count": book_page_count,
                "book_languages": book_languages,
            },
        )
        if created:
            self.stdout.write(f"Saved book: {book.book_title}")
        else:
            self.stdout.write(f"Book already exists: {book.book_title}")

    def parse_date(self, date_string):
        """
        Try to parse a date string into a Python date object.
        If parsing fails, return None.
        """
        try:
            return parser.parse(date_string).date()
        except (ValueError, TypeError):
            self.stdout.write(f"Invalid date format: {date_string}")
            return None

    def handle(self, *args, **kwargs):
        """
        Main command execution logic.
        """
        query = "self-help"  # Modify this query to fetch different types of books
        max_results = 40
        start_index = 0

        self.stdout.write("Starting to fetch and save books and authors...")

        while True:
            # Fetch a batch of books
            books = self.fetch_books_from_google(query, start_index=start_index, max_results=max_results)
            if not books:
                self.stdout.write("No more books to fetch. Exiting.")
                break

            # Process each book in the batch
            for book_data in books:
                self.save_book(book_data)

            # Move to the next batch
            start_index += max_results
            self.stdout.write(f"Processed {start_index} books so far.")
