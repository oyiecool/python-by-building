# library.py
from dataclasses import dataclass, field
from datetime import date, timedelta

LOAN_DAYS = 14
FINE_PER_DAY = 5.0

@dataclass
class Book:
    isbn: str
    title: str
    author: str
    available: bool = True

@dataclass
class Member:
    member_id: str
    name: str
    loans: dict[str, date] = field(default_factory=dict)   # isbn -> due date

class Library:
    def __init__(self):
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}

    def add_book(self, book: Book):
        self.books[book.isbn] = book

    def join(self, member: Member):
        self.members[member.member_id] = member

    def search(self, text: str) -> list[Book]:
        t = text.lower()
        return [b for b in self.books.values() if t in b.title.lower() or t in b.author.lower()]

    def checkout(self, member_id: str, isbn: str, today: date | None = None) -> date:
        today = today or date.today()
        book, member = self.books[isbn], self.members[member_id]
        if not book.available:
            raise ValueError(f"'{book.title}' is already on loan")
        if len(member.loans) >= 3:
            raise ValueError("limit of 3 books reached")
        book.available = False
        due = today + timedelta(days=LOAN_DAYS)
        member.loans[isbn] = due
        return due

    def return_book(self, member_id: str, isbn: str, today: date | None = None) -> float:
        today = today or date.today()
        member = self.members[member_id]
        due = member.loans.pop(isbn)
        self.books[isbn].available = True
        late = (today - due).days
        return max(late, 0) * FINE_PER_DAY

if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("978-0134853987", "Python Crash Course", "Eric Matthes"))
    lib.add_book(Book("978-1593279929", "Automate the Boring Stuff", "Al Sweigart"))
    lib.join(Member("M001", "Ana Cruz"))
    due = lib.checkout("M001", "978-1593279929", today=date(2026, 10, 1))
    print("Due:", due)
    fine = lib.return_book("M001", "978-1593279929", today=date(2026, 10, 20))
    print(f"Fine: {fine:.2f}")       # 5 days late -> 25.00
    print([b.title for b in lib.search("python")])
