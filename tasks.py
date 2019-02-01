import os
import urllib
import httplib, base64, json, logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from datetime import datetime as dt

import database
import connect
import models
import jinja2
import webapp2
from webapp2_extras import sessions

# remove this later
logging.basicConfig(level=logging.DEBUG)

# config for session handling
handler_config = {'webapp2_extras.sessions': {'secret_key': 'CloudComputing2019-Spotilics'}}

class Default_catch(webapp2.RequestHandler):
    def get(self):
        #perform some function
        return

class Fetch_listens(webapp2.RequestHandler):
    def get(self):
        #function to update the listens for each user in the DB
        database.init_database_connection()
        for u in database.all_users_as_list():
            update_user(u)

def update_user(user): #this is a database.User object
    access_token = connect.refresh_user_access(user.refresh_token)['access_token']
    if (user.last_check != None):
        epoch = dt.utcfromtimestamp(0)
        last_check_ms = str(int((user.last_check - epoch).total_seconds() * 1000))
        listens = connect.get_listens_after(access_token, last_check_ms)
    else:
        last_check_ms = None
        listens = connect.get_listens(access_token)
    if (listens['items'] == None): return
    features = connect.get_multi_track_features(listens)
    database.init_database_connection()
    for track, t_features in zip(listens['items'], features['audio_features']):
        if (database.track_exists(track['track']['id']) == False):
            #create a new track entry
            logging.info("Adding:")
            logging.info(track['track'])
            database.add_track(database.create_track_dict(track['track'], t_features))
        #now add a listen for the respective track
        listened_at = models.spotify_string_to_datatime(track['played_at'][:-5])
        database.add_listen(database.create_listen_dict(track['track']['id'], user.spotify_id, listened_at))
    #now need to update the users listens and last_check
    database.update_user_listens(len(listens['items']), user.spotify_id)

app = webapp2.WSGIApplication([
    ('/', Default_catch),
    ('/fetch_listens', Fetch_listens)
], debug=True, config=handler_config)
