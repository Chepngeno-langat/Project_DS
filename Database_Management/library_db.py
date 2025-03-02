import sqlite3

# define connection
connection = sqlite3.connect("library.db")

cursor = connection.cursor()

# Create tables
cursor.execute(
    """CREATE TABLE IF NOT EXISTS books(
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        year_published INTEGER,
        available_copies INTEGER DEFAULT 1
    );
    """
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS members(
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL
    );
    """
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS borrowed_books(
        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        book_id INTEGER,
        borrow_date DATE DEFAULT CURRENT_DATE,
        return_date DATE,
        FOREIGN KEY(member_id) REFERENCES members(member_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id)
    );
    """
)

connection.commit()
connection.close()

# Insert sample data
def insert_sample_data():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    
    book_data = [
        ("1984", "George Orwell", "Dystopian", 1949, 3),
        ("To Kill a Mockingbird", "Harper Lee", "Classic", 1960, 2),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, 5),
        ("The Book Thief", "Markus Zusak", "Historical Fiction", 2005, 7),
        ("The Kite Runner", "Khaled Hosseini", "Historical Fiction",2003, 2),
        ("Strange Case of Dr Jekyll and Mr Hyde", "Robert Louis Stevenson", "Gothic Horror", 1886, 5) 
    ]

    cursor.executemany("INSERT INTO books (title, author, genre, year_published, available_copies) VALUES (?, ?, ?, ?, ?)", book_data)
    
    members = [
        ("Alice Johnson", "alice@example.com", "1234567890"),
        ("Bob Smith", "bob@example.com", "0987654321")
    ]
    
    cursor.executemany("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", members)

    connection.commit()
    connection.close()

# insert_sample_data()   

# Fetch all books
def get_all_books():
    connection = sqlite3.connect("library.db")
    cursor =connection.cursor()
     
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
     
    for book in books:
        print(book)
        
    connection.close()
     
get_all_books()
    
# Borrow a book
def borrow_book(member_id, book_id):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    
    # Check if book is available
    cursor.execute("SELECT available_copies FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] > 0:
        cursor.execute("INSERT INTO borrowed_books (member_id, book_id) VALUES (?, ?)", (member_id, book_id))
        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
        connection.commit()
        print("Book Borrowed Successfully")
    else:
        print("Book is not available.")
        
    connection.close()
    
# borrow_book(1, 4)
    
# Return a book
def return_book(borrow_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Get the book_id from the borrow record
    cursor.execute("SELECT book_id FROM borrowed_Books WHERE borrow_id=?", (borrow_id,))
    book_id = cursor.fetchone()

    if book_id:
        cursor.execute("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id=?", (book_id[0],))
        cursor.execute("DELETE FROM borrowed_Books WHERE borrow_id=?", (borrow_id,))
        conn.commit()
        print("Book returned successfully!")
    else:
        print("Invalid borrow ID.")

    conn.close()

# return_book(1)  # borrow_id=1



    
