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

app = webapp2.WSGIApplication([
    ('/', Default_catch),
    ('/fetch_listens', Fetch_listens)
], debug=True, config=handler_config)
