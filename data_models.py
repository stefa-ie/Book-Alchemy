from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import foreign

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    birth_date = Column(String)
    date_of_death = Column(String)


class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(Integer)
    title = Column(String(100))
    publication_year = Column(Integer)

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', backref='books')


