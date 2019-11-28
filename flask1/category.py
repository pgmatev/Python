from database import DB
from post import Post

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def create(self):
        with DB() as db:
            db.execute('INSERT INTO categories(name) VALUES (?)', (self.name,))
            return self
        
    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM categories').fetchall()
            return [Category(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM categories WHERE id = ?', (id,)).fetchone()
            return Category(*row)

    def posts(self):
        return Post.find_by_category(self)

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM categories WHERE id = ?', (self.id,))

