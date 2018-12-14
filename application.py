#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, \
    jsonify, flash
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Movie, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

import requests

app = Flask(__name__)
APPLICATION_NAME = "Movie Catalog"

CLIENT_ID = json.loads(
    open('gp_client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# google signin function

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

        # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('gp_client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade the
         authorisation code"""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            """Token's user ID does not
            match given user ID."""),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = access_token
    login_session['id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION

    login_session['name'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one

    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    flash("Now logged in as %s" % login_session['name'])

    login_session['user_id'] = user_id
    return jsonify(name=login_session['name'],
                   email=login_session['email'],
                   img=login_session['picture'])


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received %s " % access_token)

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/' \
          'access_token?grant_type=fb_exchange_token' \
          '&client_id=%s&client_secret=%s' \
          '&fb_exchange_token=%s' % (
              app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API

    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from
         the server token exchange we have to
        split the token first on commas and select
         the first index which gives us the key : value
        for the server access token then we split it
         on colons to pull out the actual token value
        and replace the remaining quotes with nothing
         so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=' \
          '%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print("url sent for API access:%s"% url)
    # print("API JSON result: %s" % result)
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['name'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=' \
          '%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)

    login_session['user_id'] = user_id
    return jsonify(name=login_session['name'],
                   email=login_session['email'],
                   img=login_session['picture'])


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' \
          % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Create anti-forgery state token
def new_state_token():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    login_session['state'] = state
    return state


# Displays the whole movies and the genres.
@app.route('/movies.JSON')
def movies_json():
    movies = session.query(Movie).all()
    return jsonify(moives=[movie.serialize for movie in movies])


# Displays all genres
@app.route('/movies/genre/<string:genre>.json')
def movie_genre_json(genre):
    movies = session.query(Movie).filter_by(genre=genre).all()
    return jsonify(movies=[movie.serialize for movie in movies])


# Displays movies for a specific genre
@app.route('/movies/genre/<string:genre>/<int:movie_id>.json')
def movie_json(genre, movie_id):
    movie = session.query(Movie).filter_by(genre=genre, id=movie_id).first()
    return jsonify(movie=movie.serialize)


# User helper functions
def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create a new user
def create_user(login_session):
    new_user = User(
        name=login_session['name'],
        email=login_session['email'],
        picture=login_session['picture'],
        provider=login_session['provider'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# noinspection PyBroadException
def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Show all movies
@app.route('/')
@app.route('/movies/')
def show_movies():
    movies = session.query(Movie).order_by(asc(Movie.movieName))
    state = new_state_token()
    return render_template(
        'index.html',
        movies=movies,
        state=state,
        login_session=login_session)


@app.route('/movie/<string:movie_name>/')
def movie_details(movie_name):
    movie = session.query(Movie).filter_by(movieName=movie_name).one()
    get_user_id('')
    state = new_state_token()
    return render_template(
        'movie.html',
        movie=movie,
        state=state,
        login_session=login_session
    )


# Sort by movie genre
@app.route('/genre/<string:genre>/')
def sort_movies(genre):
    movies = session.query(Movie).filter_by(genre=genre).all()
    state = new_state_token()
    # Get count of genre movies
    movies_count = session.query(Movie).filter_by(genre=genre).count()
    return render_template(
        'genre.html',
        movies=movies,
        movies_count=movies_count,
        state=state,
        login_session=login_session)


# Add movie
@app.route('/movies/new', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':

        # check if user is logged in or not

        if 'provider' in login_session and \
                login_session['provider'] != 'null':
            new_movie = Movie(
                movieName=request.form['movie-name'],
                movieTrailerUrl=request.form['movie-trailer-url'],
                movieCoverUrl=request.form['movie-cover-url'],
                genre=request.form['movie-genre'],
                storyline=request.form['movie-storyline'],
                rating=request.form['movie-rating'],
                year=request.form['movie-year'],
                user_id=login_session['user_id']
            )
            session.add(new_movie)
            flash('New movie %s successfully created' % new_movie.movieName)
            session.commit()
        return redirect('/')


# Edit movie
@app.route('/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(movie_id):
    edited_movie = session.query(
        Movie).filter_by(id=movie_id).one()
    state = new_state_token()
    if request.method == 'POST':
        if request.form['movie-name']:
            edited_movie.movieName = request.form['movie-name']
        if request.form['movie-trailer-url']:
            edited_movie.movieTrailerUrl = request.form['movie-trailer-url']
        if request.form['movie-cover-url']:
            edited_movie.movieCoverUrl = request.form['movie-cover-url']
        if request.form['movie-genre']:
            edited_movie.genre = request.form['movie-genre']
        if request.form['movie-storyline']:
            edited_movie.storyline = request.form['movie-storyline']
        if request.form['movie-rating']:
            edited_movie.rating = request.form['movie-rating']
        if request.form['movie-year']:
            edited_movie.year = request.form['movie-year']

        session.add(edited_movie)
        session.commit()
        flash('Movie successfully edited %s' % edited_movie.movieName)
        return redirect('')
    else:
        return render_template('movie.html',
                               movie=edited_movie,
                               state=state,
                               login_session=login_session)


# Delete movie
@app.route('/movie/<int:movie_id>/delete', methods=['GET', 'POST'])
def delete_movie(movie_id):
    movie_to_delete = session.query(Movie).filter_by(id=movie_id).one()
    state = new_state_token()
    if request.method == 'POST':
        session.delete(movie_to_delete)
        session.commit()

        flash('Movie successfully deleted %s' % movie_to_delete.movieName)
        return redirect('/')
    else:
        return render_template('movie.html', movie=movie_to_delete,
                               state=state,
                               login_session=login_session)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['user_id']
        del login_session['name']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect('')
    else:
        flash("You were not logged in")
        return redirect('')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
