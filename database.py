import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import logging

db = SQLAlchemy()
app = Flask(__name__)

def init_database_connecton():
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
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

def add_user(data):
    # Method to add user to the database
    with app.app_context():
        user = User(**data)
        db.session.add(user)
        db.session.commit()

def user_exists(spotify_id):
    # method to check if a user is in the db
    with app.app_context():
        query = db.session.query(User).filter(User.spotify_id == spotify_id)
        result =  db.session.execute(db.session.query(query.exists()))
        return result.first()[0]

#Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    spotify_id = db.Column('spotify_id', db.String(255))
    display_name = db.Column('display_name', db.String(255))
    joined = db.Column('joined', db.DateTime())
    last_check = db.Column('last_check', db.DateTime())
    listens = db.Column('listens', db.Integer)
    refresh_token = db.Column('refresh_token', db.String(320))

    def __repr__(self):
        r_string = "User: "+self.display_name+", joined: "+self.joined+" with " + self.listens + " listens"
        return r_string

def construct_user_dict(user_info, refresh_token):
    joined = dt.now()
    user_dict = {
        'spotify_id': user_info['id'],
        'display_name': user_info['display_name'],
        'joined': joined,
        'last_check': joined,
        'listens': 0,
        'refresh_token': refresh_token
    }
    return user_dict

class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column('id', db.Integer, primary_key=True)
    spotify_id = db.Column('spotify_id', db.String(255))
    name = db.Column('name', db.String(255))
    artist = db.Column('artist', db.String(255))
    genre = db.Column('genre', db.String(255))
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

    def __repr__(self):
        r_string = "Track: " + self.name + " by " + self.artists[0]
        return r_string

class Listen(db.Model):
    __tablename__ = 'listens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, )
    track_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime())

    def __repr__(self):
        r_string = "User: " + self.id + " Listsned to track " + self.track_id
        return r_string
