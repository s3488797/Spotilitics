import os
import urllib
import httplib, base64, json, logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import database
import connect
import models
import jinja2
import webapp2
from webapp2_extras import sessions

# remove this later
logging.basicConfig(filename='example.log',level=logging.DEBUG)

# config for session handling
handler_config = {'webapp2_extras.sessions': {'secret_key': 'CloudComputing2019-Spotilics'}}

class Default_catch(webapp2.RequestHandler):
    def get(self):
        #perform some function
        return

class Fetch_listens(webapp2.RequestHandler):
    def get(self):
        #function to update the listens for each user in the DB
        for u in database.all_users_as_list():
            update_user(u)

def update_user(user): #this is a database.User object
    access_token = connect.refresh_user_access(user.refresh_token)
    last_check_ms = user.last_check.timestamp() * 1000
    listens = connect.get_listens_after(access_token, last_check_ms)
    features = connect.get_multi_track_features(listens)
    genres = connect.get_multi_track_genres(listens)
    database.init_database_connection()
    for track, t_features, t_genres in zip(listens['items'], features['audio_features'], genres):
        if (database.track_exists(track['track']['id']) == False):
            #create a new track entry
            database.add(database.Track(track['track'], t_features, t_genres))
        #now add a listen for the respective track
        database.add(database.Listen(track['track']['id'], user.id), models.spotify_string_to_datatime(track['listened_at']))
    #now need to update the users listens and last_check
app = webapp2.WSGIApplication([
    ('/', Default_catch),
    ('/fetch_listens', Fetch_listens)
], debug=True, config=handler_config)
