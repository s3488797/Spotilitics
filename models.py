from google.appengine.ext import ndb
from datetime import datetime as dt
import database as db

class Listen_model(ndb.Model):
    #model for storing a users listens
    title = ndb.StringProperty()
    artist = ndb.StringProperty()
    listened_at = ndb.DateTimeProperty()
    #genre = nbd.StringProperty() # removed because finding this would require more api requests
    explicit = ndb.BooleanProperty()
    duration_ms = ndb.IntegerProperty()
    pitch_key = ndb.IntegerProperty()
    loudness = ndb.FloatProperty()
    tempo_bpm = ndb.FloatProperty()
    acousticness = ndb.FloatProperty()
    danceability = ndb.FloatProperty()
    energy = ndb.FloatProperty()
    instrumentalness = ndb.FloatProperty()
    liveness = ndb.FloatProperty()
    speechiness = ndb.FloatProperty()
    valence = ndb.FloatProperty()

class User_model(ndb.Model):
    #Model for storing a users data
    display_name = ndb.StringProperty()
    spotify_id = ndb.StringProperty()
    joined = ndb.DateTimeProperty()
    listens_num = ndb.IntegerProperty()
    listens_list = ndb.StructuredProperty(Listen_model, repeated=True)

def construct_user(display_name, id, listens, features):
    user_model = User_model()
    user_model.display_name = display_name
    user_model.spotify_id = id
    user_model.joined = dt.now()
    user_model.listens_num = 50
    listen_data = []
    for track, feature in zip(listens['items'], features['audio_features']):
        #construct a feature object
        temp_listen = Listen_model()
        temp_listen.title = track['track']['name']
        temp_listen.artist = track['track']['artists'][0]['name']
        listened_at = track['played_at']
        listened_at = track['played_at'][:-5]
        temp_listen.listened_at = spotify_string_to_datatime(listened_at)
        temp_listen.explicit = track['track']['explicit']
        temp_listen.duration_ms = track['track']['duration_ms']
        temp_listen.pitch_key = feature['key']
        temp_listen.loudness = feature['loudness']
        temp_listen.tempo_bpm = feature['tempo']
        temp_listen.acousticness = feature['acousticness']
        temp_listen.danceability = feature['danceability']
        temp_listen.energy = feature['energy']
        temp_listen.instrumentalness = feature['instrumentalness']
        temp_listen.liveness = feature['liveness']
        temp_listen.speechiness = feature['speechiness']
        temp_listen.valence = feature['valence']
        #add it to the list
        listen_data += [temp_listen]
    user_model.listens_list = listen_data
    return user_model

def construct_user_from_db(spotify_id):
    user_db = db.get_user(spotify_id)
    user_model = User_model()
    user_model.display_name = user_db.display_name
    user_model.spotify_id = spotify_id
    user_model.joined = user_db.joined
    user_model.listens_num = user_db.listens
    listen_data = []
    listens_db = db.get_all_listens(spotify_id)
    for listen in listens_db:
        track_db = db.get_track(listen.track_id)
        #construct a feature object
        temp_listen = Listen_model()
        temp_listen.title = track_db.name
        #temp_listen.artist = track['track']['artists'][0]['name']
        listened_at = listen.timestamp
        temp_listen.explicit = track_db.explicit
        temp_listen.duration_ms = track_db.duration_ms
        temp_listen.pitch_key = track_db.pitch_key
        temp_listen.loudness = track_db.loudness
        temp_listen.tempo_bpm = track_db.tempo_bpm
        temp_listen.acousticness = track_db.q0
        temp_listen.danceability = track_db.q1
        temp_listen.energy = track_db.q2
        temp_listen.instrumentalness = track_db.q3
        temp_listen.liveness = track_db.q4
        temp_listen.speechiness = track_db.q5
        temp_listen.valence = track_db.q6
        #add it to the list
        listen_data += [temp_listen]
    user_model.listens_list = listen_data
    return user_model

def spotify_string_to_datatime(t):
    return dt.strptime(t,"%Y-%m-%dT%H:%M:%S")
