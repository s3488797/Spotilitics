# [START imports]
import os
import urllib
import httplib, base64, json, logging
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb

import database
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

class Display_default(webapp2.RequestHandler):
    def get(self):
        disp = "Connected through default url"
        template_values = {
            'message': disp
        }
        Render_template(template_values, self)

class CallBack(webapp2.RequestHandler):
    def get(self):
        display_text = DEFAULT_DISPLAY
        auth_code = self.request.get(argument_name='code')
        endpoint = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': "authorization_code",
            'code': auth_code,
            'redirect_uri': REDIRECT_URI
        }
        header_string = base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)
        headers = {
            'Authorization': 'Basic ' + header_string
        }
        post_results = urlfetch.fetch(
            url=endpoint,
            payload=urllib.urlencode(payload),
            method=urlfetch.POST,
            headers=headers
        )

        results = json.loads(post_results.content)
        if(post_results.status_code != 200):
            display_text = "An error occured, Code: " + str(post_results.status_code)
            content = post_results
            template_values = {
                'message': display_text,
                'content': results
                }
            Render_template(template_values, self)
        access_token = results['access_token']
        refresh_token = results['refresh_token']
        #need to write this new user to the databse
        template_values = {
            'message': "Successfully authenticated and Received access token"
        }
        Render_template(template_values, self)


class Login(webapp2.RequestHandler):
    def get(self):
        endpoint = "https://accounts.spotify.com/authorize"
        payload = {
            'client_id': CLIENT_ID,
            'response_type': "code",
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPES,
        }
        login_address = endpoint + "?" + urllib.urlencode(payload)
        self.redirect(login_address)

class Main(webapp2.RequestHandler):
    def get(self):
        #main space for the display of the content
        #first connect to the database
        print "placeholder\n"

app = webapp2.WSGIApplication([
    ('/', Display_default),
    ('/callback:*', CallBack),
    ('/login', Login)
], debug=True)

if __name__ == '__main__':
    #this is where the database initiation must START
    logging.info("placeholder for databse starting")
