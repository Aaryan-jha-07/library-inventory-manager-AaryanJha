import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class Book:
    title: str
    author: str
    isbn: str

    def to_dict(self):
        return asdict(self)

class LibraryInventory:
    def __init__(self, filename="library_data.json"):
        self.filepath = Path(filename)
        self.books = []
        self.load_books()

    def load_books(self):
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as file:
                    data = json.load(file)
                    # Convert dicts back to Book objects
                    self.books = [Book(**item) for item in data]
                logging.info(f"Loaded {len(self.books)} books from storage.")
            else:
                logging.info("No existing data file found. Starting fresh.")
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading data: {e}")
            self.books = []
        

    def save_books(self):
        try:
            with open(self.filepath, 'w') as file:
                # Convert all Book objects to dicts for JSON serialization
                json.dump([book.to_dict() for book in self.books], file, indent=4)
            logging.info("Data saved successfully.")
        except IOError as e:
            logging.error(f"Failed to save data: {e}")
       

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_books()
        logging.info(f"Added book: {title}")
        

    def search_by_title(self, keyword):
        results = [b for b in self.books if keyword.lower() in b.title.lower()]
        return results
        

    def find_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
        

    def display_all(self):
        return self.books
        