#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


# class to store user information
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    provider = Column(String(25))


# class for Movies Database
class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    movieName = Column(String(250), nullable=False)
    movieCoverUrl = Column(String(500), nullable=False)
    movieTrailerUrl = Column(String(500), nullable=False)
    genre = Column(String(30), nullable=False)
    storyline = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # return book data in serializable format
        return {
            'id': self.id,
            'movieName': self.movieName,
            'movieCoverUrl': self.movieCoverUrl,
            'movieTrailerUrl': self.movieTrailerUrl,
            'genre': self.genre,
            'storyline': self.storyline,
            'rating': self.rating,
            'year': self.year,
        }


engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.create_all(engine)
print("database created!")
