from database import DB
import hashlib
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = 'Bfb<jbcMbbf1^MASHm@snw2212JmM'

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def create(self):
        with DB() as db:
            values = (self.username, self.password)
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', values)
            return self

    @staticmethod    
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def find_by_username(username):
        if not username:
            return None
        with DB() as db:
            print(username)
            row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            return User(*row)

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in=600)
        return s.dumps({'username' : self.username})

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True