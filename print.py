import time
import uuid

class Book:
    def __init__(self, title, author, genre):
        self.book_id = str(uuid.uuid4())[:8]
        self.title = title
        self.author = author
        self.genre = genre
        self.is_checked_out = False
        self.due_date = None

    def __str__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f"[{self.book_id}] {self.title} by {self.author} ({self.genre}) - {status}"


class Member:
    def __init__(self, name):
        self.member_id = str(uuid.uuid4())[:8]
        self.name = name
        self.borrowed_books = []
        self.max_books = 3

    def borrow_book(self, book):
        if len(self.borrowed_books) >= self.max_books:
            return False, "Borrowing limit reached."
        if book.is_checked_out:
            return False, "Book is already checked out."
        
        self.borrowed_books.append(book)
        book.is_checked_out = True
        return True, f"Successfully borrowed '{book.title}'."

    def return_book(self, book_id):
        for book in self.borrowed_books:
            if book.book_id == book_id:
                self.borrowed_books.remove(book)
                book.is_checked_out = False
                return True, f"Successfully returned '{book.title}'."
        return False, "Book not found in your borrowed list."

    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id}) | Borrowed: {len(self.borrowed_books)}/{self.max_books}"


class Library:
    def __init__(self, name):
        self.name = name
        self.catalog = []
        self.members = {}

    def add_book(self, title, author, genre):
        new_book = Book(title, author, genre)
        self.catalog.append(new_book)
        return new_book

    def register_member(self, name):
        new_member = Member(name)
        self.members[new_member.member_id] = new_member
        return new_member

    def search_books(self, query):
        results = [book for book in self.catalog if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
        return results

    def display_catalog(self):
        print(f"\n--- {self.name} Catalog ---")
        if not self.catalog:
            print("The catalog is currently empty.")
        for book in self.catalog:
            print(book)
        print("---------------------------\n")


def main():
    # Initialize the library with some dummy data
    lib = Library("Central City Library")
    lib.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Classic")
    lib.add_book("1984", "George Orwell", "Dystopian")
    lib.add_book("Dune", "Frank Herbert", "Science Fiction")
    lib.add_book("Foundation", "Isaac Asimov", "Science Fiction")
    
    # Register a default test member
    test_member = lib.register_member("Alice Smith")

    while True:
        print(f"\nWelcome to {lib.name}")
        print("1. View Catalog")
        print("2. Search for a Book")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. View My Profile")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")

        if choice == '1':
            lib.display_catalog()

        elif choice == '2':
            query = input("Enter title or author to search: ")
            results = lib.search_books(query)
            print(f"\nFound {len(results)} matching books:")
            for b in results:
                print(b)

        elif choice == '3':
            book_id = input("Enter the Book ID you wish to borrow: ")
            target_book = next((b for b in lib.catalog if b.book_id == book_id), None)
            
            if target_book:
                success, msg = test_member.borrow_book(target_book)
                print(f"\n{msg}")
            else:
                print("\nError: Invalid Book ID.")

        elif choice == '4':
            book_id = input("Enter the Book ID you wish to return: ")
            success, msg = test_member.return_book(book_id)
            print(f"\n{msg}")

        elif choice == '5':
            print(f"\n--- Profile ---")
            print(test_member)
            if test_member.borrowed_books:
                print("Currently Borrowed:")
                for b in test_member.borrowed_books:
                    print(f" - {b.title}")
            print("---------------")

        elif choice == '6':
            print("Exiting library system. Goodbye!")
            break

        else:
            print("Invalid input. Please try again.")
            
        time.sleep(1)

if __name__ == "__main__":
    main()