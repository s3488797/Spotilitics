import os
import urllib
import httplib, base64, json, logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from datetime import timedelta as td
from datetime import datetime as dt
import database
import connect
import models
import tasks
import jinja2
import webapp2
from webapp2_extras import sessions

# remove this later
logging.basicConfig(filename='example.log',level=logging.DEBUG)

DEFAULT_DISPLAY = "Heading"

WELCOME_DISPLAY = "html/welcome.html"
MAIN_DISPLAY = "html/analyse.html"
DEBUG_DISPLAY = "html/debug.html"
DEFAULT_TEMPLATE = {'message': "Welcome"}

# config for session handling
handler_config = {'webapp2_extras.sessions': {'secret_key': 'CloudComputing2019-Spotilics'}}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# This is a handler that will initiate a session for other handlers that need it
class Session_handler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try: #we use a try here so that once the request is complete we can save the session data
            webapp2.RequestHandler.dispatch(self)
        finally: # we then save the session when the request is complete
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

def render_template(handler, template_values=DEFAULT_TEMPLATE, display=WELCOME_DISPLAY):
    template = JINJA_ENVIRONMENT.get_template(display)
    handler.response.write(template.render(template_values))

class Default_catch(Session_handler):
    def get(self):
        if (self.session.get('active_user') == None):
            self.redirect('/welcome')
        else:
            logging.info("Detected that the current user is already logged in")
            self.redirect('/main')

class Welcome(Session_handler):
    def get(self):
        if (self.session.get('active_user') == None):
            render_template(self, display=WELCOME_DISPLAY)
        else:
            logging.info("Detected that the current user is already logged in")
            self.redirect('/main')

class Main(Session_handler):
    def get(self):
        # load some values from the session
        display_name = self.session.get('active_user')
        if (display_name == None):
            logging.info("Detected noone was logged in")
            self.redirect('/welcome')
            return
        database.init_database_connection()
        #ok now construct our user model
        user_model = models.construct_user_from_db(self.session.get('active_user'))
        template_values = {
            'message': "Got these features for " + display_name,
            'user': user_model
        }
        render_template(self, template_values, MAIN_DISPLAY)

class CallBack(Session_handler):
    def get(self):
        if (self.request.get(argument_name='error') == 'access_denied'):
            self.redirect('/decline')
            return
        #the user has authorised access
        auth_token = self.request.get(argument_name='code')
        access_request = connect.request_user_access(auth_token)
        if (access_request == False):
            self.redirect('/error')
            return
        #now get info about the current user
        access_token = access_request['access_token']
        refresh_token = access_request['refresh_token']
        user_info = connect.get_user_data(access_token)
        if (user_info == False):
            self.redirect('/error')
            return
        #now we need to write a cookie so that the server isnt always requesting to spotify
        # write info to the session so it can be picked up easy later
        self.session['active_user'] = user_info['id']
        self.session['access_token'] = access_token
        self.session['refresh_token'] = refresh_token
        user_data_to_add = database.construct_user_dict(user_info, refresh_token)
        #check if the user is already in the db
        database.init_database_connection()
        #if (database.user_exists(user_info['id']) == True):
            #database.update_user_refresh(refresh_token, user_info['id'])
        if (database.user_exists(user_info['id']) == False):
            #create dict of user data
            if (database.add_user(user_data_to_add) == False):
                self.redirect('/error')
                return
        # now record the first data for the user
        #tasks.update_user(database.get_user(user_info['id']))
        # now go to the main page
        self.redirect('/main')


class Login(webapp2.RequestHandler):
    def get(self):
        # redirect to the spotify authorization page
        self.redirect(connect.login_address())

class Logout(Session_handler):
    def get(self):
        # remove the session and return the welcome page
        self.session.clear()
        self.redirect('/welcome')

class Declined(webapp2.RequestHandler):
    def get(self):
        #the page to display when the user has declided access
        template_values = {'message': "access was declided"}
        render_template(self, template_values, WELCOME_DISPLAY)

class Error_occured(webapp2.RequestHandler):
    def get(self):
        #the page to display when the user has declided access
        template_values = {'message': "An error occured at some point, check the logs"}
        render_template(self, template_values, DEBUG_DISPLAY)

class Init_db(webapp2.RequestHandler):
    def get(self):
        database.init_database_connection()
        database.create_tables()
        template_values = {'message': "Attempting to init the database"}
        render_template(self, template_values, DEBUG_DISPLAY)

class Debug(Session_handler):
    def get(self):
        database.init_database_connection()
        #ok now construct our user model
        user_model = models.construct_user_from_db("ladecaz")
        template_values = {
            'message': "Got these for Environment variables",
            'content': user_model
        }
        database.close_connection()
        render_template(self, template_values, DEBUG_DISPLAY)

app = webapp2.WSGIApplication([
    ('/', Default_catch),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/main', Main),
    ('/logout', Logout),
    ('/callback:*', CallBack),
    ('/decline', Declined),
    ('/error', Error_occured),
    ('/init_db', Init_db),
    ('/debug', Debug)
], debug=True, config=handler_config)
