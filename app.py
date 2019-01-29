import os
import urllib
import httplib, base64, json, logging
import datetime
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import database
import connect
import jinja2
import webapp2


DEFAULT_DISPLAY = "Heading"
CLIENT_ID = "4f2c1f999a4c480f9d9eea2f82b53723"
CLIENT_SECRET = "ba1c5975884d4ba080e84b8540b1bc6a"
REDIRECT_URI = "https://s3488797-cc2019.appspot.com/callback"
SCOPES = "user-read-private user-read-recently-played user-read-currently-playing"
encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def Render_template(template_values, handler):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    handler.response.write(template.render(template_values))

class Main(webapp2.RequestHandler):
    def get(self):
        disp = "Connected through default url"
        template_values = {
            'message': disp
        }
        Render_template(template_values, self)

class CallBack(webapp2.RequestHandler):
    def get(self):
        if (self.request.get(argument_name='error') != 'access_denied'):
            #the user has authorised access
            auth_token = self.request.get(argument_name='code')
            results = connect.request_access(auth_token)
            if (results == False): self.redirect('/error')
        else:
            #the user has declined
            self.redirect('/decline')
        #now get info about the current user
        access_token = results['access_token']
        user_info = connect.get_user_data(access_token)
        if (user_info == False): self.redirect('/error')
        #create dict of user data
        refresh_token = results['refresh_token']
        user_data_to_add = {
            'spotify_id': user_info['id'],
            'display_name': user_info['display_name'],
            'joined': datetime.datetime.now(),
            'last_check': datetime.datetime.now(),
            'listens': 0,
            'auth_token': self.request.get(argument_name='code'),
            'refresh_token': refresh_token
        }
        #need to write this new user to the databse
        database.init_database_connecton()
        if (database.add_user(user_data_to_add) == False): self.redirect('/error')
        #now lets get some listen data and send it to the html
        listens = connect.get_listens(access_token)
        if (listens == False): self.redirect('/error')
        # First construct a list of ids to get details for
        id_string_list = ""
        for track in listens['items']:
            id_string_list += track['track']['id'] + ","
        id_string_list.strip(',')
        #now get the details of this list
        features = connect.get_multi_track_features(id_string_list)
        if (features == False): self.redirect('/error')
        #ok now construct our models
        template_values = {
            'message': "Got these features for " + user_info['display_name'],
            'content': features
        }
        Render_template(template_values, self)


class Login(webapp2.RequestHandler):
    def get(self):
        target = connect.login_address()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("redirecting to: " + target)
        self.redirect(target)

class Declined(webapp2.RequestHandler):
    def get(self):
        #the page to display when the user has declided access
        template_values = {
            'message': "access was declided"
        }
        Render_template(template_values, self)

class Error_occured(webapp2.RequestHandler):
    def get(self):
        #the page to display when the user has declided access
        template_values = {
            'message': "An error occured at some point, check the logs"
        }
        Render_template(template_values, self)

class Init_db(webapp2.RequestHandler):
    def get(self):
        database.init_database_connecton()
        database.create_tables()
        template_values = {
            'message': "Attempting to init the database"
        }
        Render_template(template_values, self)

app = webapp2.WSGIApplication([
    ('/', Login),
    ('/login', Login),
    ('/main', Main),
    ('/callback:*', CallBack),
    ('/decline', Declined),
    ('/error', Error_occured),
    ('/init_db', Init_db) #REMOVE THIS LATER
], debug=True)
