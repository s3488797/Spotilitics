# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

DEFAULT_DISPLAY = "Heading"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def Render_template(template_values, handler):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    handler.response.write(template.render(template_values))

class Display1(webapp2.RequestHandler):
    def get(self):
        display1_text = "Connected through Display 1"
        template_values = {
            'message': display1_text
        }
        Render_template(template_values, self)

class Display2(webapp2.RequestHandler):
    def get(self):
        display2_text = "Connect through Display 2"
        template_values = {
            'message': display2_text
        }
        Render_template(template_values, self)

class Display_default(webapp2.RequestHandler):
    def get(self):
        disp = "Connected through default url"
        template_values = {
            'message': disp
        }
        Render_template(template_values, self)

class Data_return(webapp2.RequestHandler):
    def get(self):
        display_text = DEFAULT_DISPLAY
        data_content = self.request.get()
        template_values = {
            'message': display_text,
            'content':
        }

app = webapp2.WSGIApplication([
    ('/', Display_default),
    ('/1', Display1),
    ('/2', Display2),
    ('/return', Data_return),
], debug=True)
