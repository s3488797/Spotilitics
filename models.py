from google.appengine.ext import ndb
from datetime import datetime as dt

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
    joined = ndb.DateTimeProperty()
    listens_num = ndb.IntegerProperty()
    listens_list = ndb.StructuredProperty(Listen_model, repeated=True)

def construct_user(display_name, listens, features):
    user_model = User_model()
    user_model.display_name = display_name
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
        temp_listen.listened_at = dt.strptime(listened_at,"%Y-%m-%dT%H:%M:%S")
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
