import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book


app = Flask(__name__)

DB_DIR = "/Users/Work/PycharmProjects/Book Alchemy/data"
DB_PATH = os.path.join(DB_DIR, 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

db.init_app(app)

'''with app.app_context():
  db.create_all()'''


@app.route('/')
def index():
  """
  Displays all books with title, author, ISBN and cover one below the other.
  """
  books = Book.query.all()
  return render_template('home.html', books=books), 200


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
  """
  Displays a form for user to add an author with information
  about name, birthdate and date of death.
  """
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
  """
  Displays a form for user to add a book with information
  about title, ISBN, publication year and author.
  Author can be selected from a dropdown list.
  """
  authors = Author.query.all()
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


@app.route('/sorting')
def sorting():
  """
  Allows the user to sort in ascending order by title or by author.
  """
  sort_by = request.args.get('sort_by', 'title')  # Default sorting by title

  if sort_by == 'title':
    books = Book.query.order_by(Book.title.asc())
  elif sort_by == 'author':
    books = Book.query.join(Author).order_by(Author.name.asc())
  else:
    books = Book.query.order_by(Book.title.asc()).all()  # Default sorting

  authors = Author.query.order_by(Author.name.asc()).all()

  return render_template('home.html', books=books, authors=authors, sort_by=sort_by)


@app.route('/search', methods=['POST'])
def search():
  """
  Allows the user to place a keyword search within book titles or author names.
  """
  search = request.form.get('search').strip()
  books = []
  authors = []

  if search:
    books = (
      Book.query
      .join(Author)
      .filter(
        Book.title.ilike(f"%{search}%") |  # Search in book titles
        Author.name.ilike(f"%{search}%")  # Search in author names
      )
      .all()
    )

    message = None
    if not books:
      message = f'No books or authors found matching "{search}".'


  return render_template('home.html', books=books, authors=authors, search_query=search, message=message)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete(book_id):
  """
  Deletes a book, and if the author has no other books left in the library, the author is also removed.
  """
  book = Book.query.get_or_404(book_id)
  author = book.author

  db.session.delete(book)
  db.session.commit()

  left_num_books_by_author = Book.query.filter_by(author_id=author.id).count()
  if left_num_books_by_author == 0:
    db.session.delete(author)
    db.session.commit()

    return f"Book {book.title} and {author.name} have been deleted successfully."

  return f"Book {book.title} has been deleted successfully."



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)