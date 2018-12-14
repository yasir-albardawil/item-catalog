#!/usr/bin/env python3

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from database_setup import Base, Movie, User

engine = create_engine('sqlite:///item_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create user
User1 = User(name="Yasir Albardawil", email="yasir.s.albardawil@gmail.com")
session.add(User1)
session.commit()

# movie data
movie1 = Movie(movieName="The Shawshank Redemption",
               movieCoverUrl="https://m.media-amazon.com/images/M"
                             "/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRl"
                             "YWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_"
                             ".jpg",
               movieTrailerUrl="https://www.imdb.com/videoembed/vi3877612057",
               genre="drama",
               storyline="Chronicles the experiences of a formerly successful"
                         " banker as a prisoner in the gloomy "
                         "jailhouse of Shawshank after being found guilty of"
                         " a crime he did not commit. The film "
                         "portrays the man's unique way of dealing with his"
                         " new, torturous life; along the way he "
                         "befriends a number of fellow prisoners, most"
                         " notably a wise long-term inmate named Red. "
                         "Written by J-S-Golden",
               rating=9.3,
               year=1994,
               user_id=1)

session.add(movie1)
session.commit()

# movie data
movie2 = Movie(movieName="Big Hero 6",
               movieCoverUrl="https://m.media-amazon.com/images/M"
                             "/MV5BMDliOTIzNmUtOTllOC00NDU3LWFiNjYtMGM0ND"
                             "c1YTMxNjYxXkEyXkFqcGdeQXVyNTM3NzExMDQ"
                             "@._V1_SY1000_CR0,0,699,1000_AL_.jpg",
               movieTrailerUrl="https://www.youtube.com/embed/z3biFxZIJOQ",
               genre="animation",
               storyline="When a devastating event befalls the city"
                         " of San Fransokyo and catapults Hiro into the "
                         "midst of danger, he turns to Baymax and his close"
                         " friends adrenaline junkie Go Go Tomago, "
                         "neatnik Wasabi, chemistry whiz Honey Lemon and"
                         " fanboy Fred. Determined to uncover the "
                         "mystery, Hiro transforms his friends into a band "
                         "of high-tech heroes called \"Big Hero 6.\" "
                         "Written by Walt Disney Animation Studios",
               rating=7.8,
               year=2014,
               user_id=1)

session.add(movie2)
session.commit()

# movie data
movie3 = Movie(movieName="IT",
               movieCoverUrl="https://m.media-amazon.com/images/M"
                             "/MV5BZDVkZmI0YzAtNzdjYi00ZjhhLWE1ODEtMWMzMW"
                             "MzNDA0NmQ4XkEyXkFqcGdeQXVyNzYzODM3Mzg"
                             "@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
               movieTrailerUrl="https://www.imdb.com/videoembed/vi1396095257",
               genre="horror",
               storyline="In the Town of Derry, the local kids are "
                         "disappearing one by one. In a place known as 'The "
                         "Barrens', a group of seven kids are united by"
                         " their horrifying and strange encounters with "
                         "an evil clown and their determination to "
                         "kill It. Written by Emma Chapman",
               rating="7.4",
               year=2017,
               user_id=1)

session.add(movie3)
session.commit()

# movie data
movie4 = Movie(movieName="Hacker",
               movieCoverUrl="https://m.media-amazon.com/images/M"
                             "/MV5BYjk3ZWQ4ZmMtNzM1OS00NDQxLWJmZjctNzF"
                             "lODAyODRkMjcyXkEyXkFqcGdeQXVyMjEwODIzODA"
                             "@._V1_SY1000_CR0,0,748,1000_AL_.jpg",
               movieTrailerUrl="https://www.youtube.com/embed/y8HsD9qmTiY",
               genre="crime",
               storyline="When his family hits financial trouble, Alex"
                         " Danyliuk turns to a life of crime and identity "
                         "theft, with the help of Sye, a street-wise"
                         " hustler who introduces him to the world of black "
                         "market trading, Kira, a young female hacker,"
                         " and contacts on the dark web. After finding "
                         "success in causing financial market chaos,"
                         " they gain the attention of Z, a mysterious "
                         "masked figure, who's the head of an organization"
                         " known as Anonymous, and a number one "
                         "target by the FBI, Written by Mitch Swan",
               rating="6.2",
               year=2016,
               user_id=1)

session.add(movie4)
session.commit()
print("added Movies!")
