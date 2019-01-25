import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_databse():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("All Created")

#Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    spotify_id = db.Column('spotify_id', db.String(255))
    display_name = db.Column('display_name', db.String(255))
    joined = db.Column('joined', db.DateTime())
    last_check = db.Column('last_check', db.DateTime())
    listens = db.Column('listens', db.Integer)
    auth_token = db.Column('auth_token', db.String(255))
    refresh_token = db.Column('refresh_token', db.String(255))

    def __repr__(self):
        r_string = "User: "+self.display_name+", joined: "+self.joined+" with " + self.listens + " listens"
        return r_string

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
    q0 = db.Column('accousticness', db.Integer)
    q1 = db.Column('danceability', db.Integer)
    q2 = db.Column('energy', db.Integer)
    q3 = db.Column('intrumentalness', db.Integer)
    q4 = db.Column('liveness', db.Integer)
    q5 = db.Column('speechiness', db.Integer)
    q6 = db.Column('valence', db.Integer)

    def __repr__(self):
        r_string = "Track: " + self.name + " by " + self.artists[0]
        return r_string

class Listen(db.Model):
    __tablename__ = 'listens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    track_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime())

    def __repr__(self):
        r_string = "User: " + self.id + " Listsned to track " + self.track_id
        return r_string
