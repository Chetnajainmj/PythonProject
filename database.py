import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("book_reviews.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Create reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_title TEXT,
            review TEXT,
            rating INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Add a new user
def register_user(username, password):
    conn = sqlite3.connect("book_reviews.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("book_reviews.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# Add a new review
def add_review(user_id, book_title, review, rating):
    conn = sqlite3.connect("book_reviews.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (user_id, book_title, review, rating) VALUES (?, ?, ?, ?)",
                   (user_id, book_title, review, rating))
    conn.commit()
    conn.close()

# Fetch all reviews for a book
def get_reviews(book_title):
    conn = sqlite3.connect("book_reviews.db")
    cursor = conn.cursor()
    cursor.execute("SELECT review, rating FROM reviews WHERE book_title=?", (book_title,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews