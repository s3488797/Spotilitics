from google.appengine.ext import ndb

class User_model(ndb.Model):
    #Model for storing a users data
    display_name = ndb.StringProperty()
    joined = ndb.DateTimeProperty()
    listens_num = ndb.IntegerProperty()
    listens_list = ndb.StructuredProperty(Listen_model, repeated=True)

class Listen_model(ndb.Model):
    #model for storing a users listens
    title = ndb.StringProperty()
    artist = ndb.StringProperty()
    listened_at = ndb.DateTimeProperty()
    genre = nbd.StringProperty()
    explicit = ndb.BooleanProperty()
    duration_ms = ndb.IntegerProperty()
    pitch_key = ndb.IntegerProperty()
    loudness = ndb.IntegerProperty()
    tempo_bpm = ndb.IntegerProperty()
    accousticness = ndb.FloatProperty()
    danceability = ndb.FloatProperty()
    energy = ndb.FloatProperty()
    intrumentalness = ndb.FloatProperty()
    liveness = ndb.FloatProperty()
    speechiness = ndb.FloatProperty()
    valence = ndb.FloatProperty()
