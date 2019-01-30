from google.appengine.ext import ndb

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
