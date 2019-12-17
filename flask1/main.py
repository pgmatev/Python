from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
from flask_httpauth import HTTPBasicAuth
import json
from functools import wraps

from post import Post
from comment import Comment
from category import Category
from user import User
import database

app = Flask(__name__)
auth = HTTPBasicAuth()

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def hello_world():
    return redirect(url_for('list_posts'))

@app.route('/posts')
def list_posts():
    return render_template('posts.html', posts=Post.all())

@app.route('/posts/<int:id>')
def show_post(id):
    post = Post.find(id)

    return render_template('post.html', post=post)

@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.find(id)
    if request.method == 'GET':

        return render_template('edit_post.html', post=post)
    elif request.method == 'POST':
        post.name = request.form['name']
        post.author = request.form['author']
        post.content = request.form['content']
        post.save()
        return redirect(url_for('show_post', id=post.id))

@app.route('/posts/new', methods=['GET', 'POST'])
@require_login
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', categories=Category.all())
    elif request.method == 'POST':
        category = Category.find(request.form['category'])
        values = (None, request.form['name'], request.form['author'], request.form['content'], category)
        Post(*values).create()

        return redirect(url_for('list_posts'))

@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.find(id)
    post.delete()

    return redirect(url_for('list_posts'))

@app.route('/comments/new', methods=['POST'])
def new_comment():
    if request.method == 'POST':
        post = Post.find(request.form['post_id'])
        values = (None, post, request.form['message'])
        Comment(*values).create()

        return redirect(url_for('show_post', id=post.id))

@app.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    if request.method == 'GET':
        return render_template('new_category.html')
    elif request.method == 'POST':
        values = (None, request.form['name'])
        Category(*values).create()
        
        return redirect(url_for('list_categories'))

@app.route('/categories')
def list_categories():
    return render_template('categories.html', categories=Category.all())

@app.route('/categories/<int:id>')
def show_category(id):
    category = Category.find(id)
    return render_template('category.html', category=category)

@app.route('/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    category = Category.find(id)
    category.delete()
    return redirect('/categories')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (None, request.form['username'], User.hash_password(request.form['password']))
        User(*values).create()

        return redirect('/')

@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)
    if user:
        return user.verify_password(password)
    return False

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token})

        




if __name__ == '__main__':
    app.run()
