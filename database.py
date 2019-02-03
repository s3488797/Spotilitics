import os
import config
from sqlalchemy.sql import schema
from sqlalchemy import types
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import logging

db = SQLAlchemy()
app = Flask(__name__)

def init_database_connection():
    app.config.from_pyfile('config.py')
    with app.app_context():
        db.init_app(app)
    logging.info("All Created")

def create_tables():
    with app.app_context():
        db.create_all()

def close_connection():
    with app.app_context():
        db.dispose()

def sql_to_dict(row):
    # Translates a SQLAlchemy model instance into a dictionary
    with app.app_context():
        data = row.__dict__.copy()
        data['id'] = row.id
        data.pop('_sa_instance_state')
    return data

# ADD methods, I really dont like these and would much rather get __init__ working
# Method to add user to the database
def add_user(data):
    with app.app_context():
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

def add_track(data):
    with app.app_context():
        track = Track(**data)
        db.session.add(track)
        db.session.commit()
        return track

def add_listen(data):
    with app.app_context():
        listen = Listen(**data)
        db.session.add(listen)
        db.session.commit()
        return listen

def add(object):
    with app.app_context():
        db.session.add(object)
        db.session.commit()
        return object

def entry_exists(type, spotify_id):
    with app.app_context():
        query = db.session.query(type).filter(type.spotify_id == spotify_id)
        result =  db.session.execute(db.session.query(query.exists()))
        return result.first()[0]

# method to check if a user is in the db
def user_exists(spotify_id):
    return entry_exists(User, spotify_id)

# method to check a track exists
def track_exists(spotify_id):
    return entry_exists(Track, spotify_id)

#method to retrieve all users as objects
def all_users_as_list():
    with app.app_context():
        users = User.query.all()
        return users

# method to get all listens of a user
def get_all_listens(spotify_id):
    with app.app_context():
        return Listen.query.filter(Listen.user_id == spotify_id).all()

# method to retrieve user by id
def get_user(spotify_id):
    with app.app_context():
        return User.query.filter(User.spotify_id == spotify_id).first()

def get_track(spotify_id):
    with app.app_context():
        return Track.query.filter(Track.spotify_id == spotify_id).first()

def get_user_test(spotify_id):
    with app.app_context():
        query = db.session.query(User).filter(User.spotify_id == spotify_id)
        result =  db.session.execute(db.session.query(query.exists()))
        return result.first()

def update_user_listens(new_listens, spotify_id):
    with app.app_context():
        user = db.session.query(User).filter(User.spotify_id == spotify_id).first()
        user.listens += new_listens
        user.last_check = dt.now()
        db.session.commit()

#Models
class User(db.Model):
    __tablename__ = 'users'
    spotify_id = db.Column('spotify_id', db.String(255), primary_key=True, unique=True)
    display_name = db.Column('display_name', db.String(255))
    joined = db.Column('joined', db.DateTime())
    last_check = db.Column('last_check', db.DateTime(), nullable=True)
    listens = db.Column('listens', db.Integer)
    refresh_token = db.Column('refresh_token', db.String(320))


def construct_user_dict(user_info, refresh_token):
    joined = dt.now()
    user_dict = {
        'spotify_id': user_info['id'],
        'display_name': user_info['display_name'],
        'joined': joined,
        'last_check': None,
        'listens': 0,
        'refresh_token': refresh_token
    }
    return user_dict

class Track(db.Model):
    __tablename__ = 'tracks'
    spotify_id = db.Column('spotify_id', db.String(255), primary_key=True, unique=True)
    name = db.Column('name', db.String(255))
    #artists = db.Column('artists', types.ARRAY(db.String(255)))# TODO This is currently not accepted
    #album = db.Column('album', db.String(255))
    #genre = db.Column('genre', types.ARRAY(db.String(255))) # TODO This is currently not accepted
    popularity = db.Column('popularity', db.Integer)
    explicit = db.Column('explicit', db.Boolean)
    duration_ms = db.Column('duration_ms', db.Integer)
    pitch_key = db.Column('pitch_key', db.Integer)
    loudness = db.Column('loudness', db.Integer)
    tempo_bpm = db.Column('tempo_bpm', db.Integer)
    q0 = db.Column('acousticness', db.Float)
    q1 = db.Column('danceability', db.Float)
    q2 = db.Column('energy', db.Float)
    q3 = db.Column('instrumentalness', db.Float)
    q4 = db.Column('liveness', db.Float)
    q5 = db.Column('speechiness', db.Float)
    q6 = db.Column('valence', db.Float)

    #this constructor specifily accepts the spotify API models
def create_track_dict(spotify_track, t_feature, genres=None):
    data_dict = {
        'spotify_id': spotify_track['id'],
        'name': spotify_track['name'],
        'popularity': spotify_track['popularity'],
        'explicit': spotify_track['explicit'],
        'duration_ms': spotify_track['duration_ms'],
        'pitch_key': t_feature['key'],
        'loudness': t_feature['loudness'],
        'tempo_bpm': t_feature['tempo'],
        'q0': t_feature['acousticness'],
        'q1': t_feature['danceability'],
        'q2': t_feature['energy'],
        'q3': t_feature['instrumentalness'],
        'q4': t_feature['liveness'],
        'q5': t_feature['speechiness'],
        'q6': t_feature['valence']
    }
    return data_dict

def create_user_test(spotify_track, t_feature, genres=None):
    u = User()
    u.spotify_id = spotify_track['id']
    u.name = spotify_track['name']
    #u.artists = [artist['name'] for artist in track['artists']]
    #u.album = track['album']['name']
    #u.genres = genres
    u.popularity = spotify_track['popularity']
    u.explicit = spotify_track['explicit']
    u.duration_ms = spotify_track['duration_ms']
    u.pitch_key = t_feature['key']
    u.loudness = t_feature['loudness']
    u.tempo_bpm = t_feature['tempo']
    u.q0 = t_feature['acousticness']
    u.q1 = t_feature['danceability']
    u.q2 = t_feature['energy']
    u.q3 = t_feature['instrumentalness']
    u.q4 = t_feature['liveness']
    u.q5 = t_feature['speechiness']
    u.q6 = t_feature['valence']
    return u

class Listen(db.Model):
    __tablename__ = 'listens'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(255), schema.ForeignKey("users.spotify_id"), nullable=False)
    track_id = db.Column('track_id', db.String(255), schema.ForeignKey("tracks.spotify_id"), nullable=False)
    timestamp = db.Column('timestamp', db.DateTime())

    #def __init__(t_id, u_id, time):
    #    self.user_id = u_id
    #    self.track_id = t_id
    #    self.timestamp = time
    #    return self

def create_listen_dict(t_id, u_id, time):
    data_dict = {
        'user_id': u_id,
        'track_id': t_id,
        'timestamp': time
    }
    return data_dict
