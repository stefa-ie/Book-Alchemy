from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

db = SQLAlchemy()

# Create a database connection
engine = create_engine('sqlite:///data/library.sqlite')

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    birth_date = Column(String)
    date_of_death = Column(String)

    book = relationship('Book', back_populates='author')

    def __repr__(self):
        return f"(id = {self.id}, name = {self.name}, birth_date = {self.birth_date}, date_of_death = {self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(Integer)
    title = Column(String(100))
    publication_year = Column(Integer)

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='book')

    def __repr__(self):
        return f"(id = {self.id}), isbn = {self.isbn}, title = {self.title}, publication_year = {self}.publication_year)"

