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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
