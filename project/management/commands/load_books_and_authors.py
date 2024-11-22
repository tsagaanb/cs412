import requests
from django.core.management.base import BaseCommand
from project.models import Author, Book
from dateutil import parser


class Command(BaseCommand):
    help = "Load books and authors from Google Books API into the database"

    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
    API_KEY = "AIzaSyDlKkk-tLl71yvjuolcGBnbpdfCO7JI_po"  # Replace with your Google API key

    def fetch_books(self, query, start_index=0, max_results=40):
        """
        Fetch books from Google Books API using a query.
        """
        params = {
            "q": query,
            "startIndex": start_index,
            "maxResults": max_results,
            "key": self.API_KEY,
        }
        response = requests.get(self.GOOGLE_BOOKS_API_URL, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            self.stdout.write(f"Failed to fetch data: {response.status_code}")
            return []

    def save_author(self, author_name):
        """
        Save an author to the database, avoiding duplicates.
        """
        # Split the author's name into first and last names
        name_parts = author_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Save or retrieve the author
        author, created = Author.objects.get_or_create(
            author_first_name=first_name,
            author_last_name=last_name,
        )
        if created:
            self.stdout.write(f"Saved author: {author}")
        return author

    def save_book(self, book_data):
        """
        Save a book to the database, avoiding duplicates.
        """
        # Extract book details
        volume_info = book_data.get("volumeInfo", {})
        book_name = volume_info.get("title", "Untitled")
        book_subjects = ', '.join(volume_info.get("categories", []))
        book_description = volume_info.get("description", "")
        book_publish_date = self.parse_book_date(volume_info.get("publishedDate", ""))
        book_cover_image = volume_info.get("imageLinks", {}).get("thumbnail", None)
        book_page_count = volume_info.get("pageCount", None)
        book_languages = volume_info.get("language", "")

        # Handle the first author only
        authors = volume_info.get("authors", [])
        if authors:
            author_name = authors[0]
            author = self.save_author(author_name)
        else:
            self.stdout.write(f"No author found for book: {book_name}")
            return

        # Save or retrieve the book
        book, created = Book.objects.get_or_create(
            book_name=book_name,
            book_author=author,
            defaults={
                "book_subjects": book_subjects,
                "book_description": book_description,
                "book_publish_date": book_publish_date,
                "book_cover_image": book_cover_image,
                "book_page_count": book_page_count,
                "book_languages": book_languages,
            },
        )
        if created:
            self.stdout.write(f"Saved book: {book.book_name}")
        else:
            self.stdout.write(f"Book already exists: {book.book_name}")

    def parse_book_date(self, date_string):
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
        query = "fiction"  # Modify this query to fetch different types of books
        max_results = 40
        start_index = 0

        self.stdout.write("Starting to fetch and save books and authors...")

        while True:
            # Fetch a batch of books
            books = self.fetch_books(query, start_index=start_index, max_results=max_results)
            if not books:
                self.stdout.write("No more books to fetch. Exiting.")
                break

            # Process each book in the batch
            for book_data in books:
                self.save_book(book_data)

            # Move to the next batch
            start_index += max_results
            self.stdout.write(f"Processed {start_index} books so far.")
