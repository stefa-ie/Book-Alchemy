import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book, session

app = Flask(__name__)

DB_DIR = "/Users/Work/PycharmProjects/Book Alchemy/data"
DB_PATH = os.path.join(DB_DIR, 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

db.init_app(app)

'''with app.app_context():
  db.create_all()'''


@app.route('/')
def index():
  books = Book.query.all()
  return render_template('home.html', books=books), 200


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
  if request.method == 'GET':
    return render_template('add_author.html'), 200

  if request.method == 'POST':
    author_name = request.form.get('name')
    birth_date = request.form.get('birthdate')
    date_death = request.form.get('date_of_death')

    author = Author(
      name=author_name,
      birth_date=birth_date,
      date_of_death=date_death
    )

    db.session.add(author)
    db.session.commit()

    return f"New author {author_name} has been added successfully."


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
  authors = Author.query.all()  # Fetch all authors
  if request.method == 'GET':
      return render_template('add_book.html', authors=authors), 200

  if request.method == 'POST':
    title = request.form['title']
    isbn = request.form['isbn']
    publication_year = request.form['publication_year']
    author_id = request.form['author_id']

    if not author_id:
      return "Please select an author.", 400

    author = Author.query.get(author_id)
    if not author:
      return "Author does not exist.", 400

    book = Book(
      title=title,
      isbn=isbn,
      publication_year=publication_year,
      author_id=author_id
    )

    db.session.add(book)
    db.session.commit()

    return f"New book '{title}' has been added successfully.", 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)