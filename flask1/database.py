import sqlite3

DB_NAME = 'example.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS posts 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, author TEXT,
        content TEXT,
        category_id INTEGER NOT NULL, 
        FOREIGN KEY (category_id) REFERENCES categories(id)
    
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS comments
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        message TEXT,
        FOREIGN KEY(post_id) REFERENCES posts(id)
    )
''')

conn.cursor().execute('CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')

conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()

