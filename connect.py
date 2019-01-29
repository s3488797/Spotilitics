import os
import urllib
import httplib, base64, json, logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import jinja2
import webapp2


DEFAULT_DISPLAY = "Heading"
CLIENT_ID = "4f2c1f999a4c480f9d9eea2f82b53723"
CLIENT_SECRET = "ba1c5975884d4ba080e84b8540b1bc6a"
REDIRECT_URI = "https://s3488797-cc2019.appspot.com/callback"
SCOPES = "user-read-private user-read-recently-played user-read-currently-playing"
client_details = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)

def login_address():
    #""""Function to create link for user auth"""
    endpoint = "https://accounts.spotify.com/authorize"
    payload = {
        'client_id': CLIENT_ID,
        'response_type': "code",
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
    }
    target = endpoint + "?" + urllib.urlencode(payload)
    return target

def make_request(endpoint, method, headers, payload=None):
    #Function to make fetch requests
    fetch_results = urlfetch.fetch(
        url=endpoint,
        payload=payload,
        method=method,
        headers=headers
    )
    logging.info("Received: ")
    logging.info(fetch_results)
    results = json.loads(fetch_results.content)
    logging.info("Containing: ")
    logging.info(results)
    if (fetch_results.status_code != 200):
        error_string = "Error occured making " + str(method) + " request"
        if (method == urlfetch.POST):
            error_string += ": " + results['error_description']
        logging.error(error_string)
        return False
    return results

def request_access(auth_code):
    # Initial request for access of a user
    endpoint = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': "authorization_code",
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Authorization': 'Basic ' + client_details
    }
    return make_request(
        endpoint,
        urlfetch.POST,
        headers,
        urllib.urlencode(payload)
    )

def request_refresh(refresh_token):
    #"""Request for an access token using a refresh token"""
    endpoint = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': "refresh_token",
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': 'Basic ' + client_details
    }
    return make_request(
        endpoint,
        urlfetch.POST,
        headers,
        urllib.urlencode(payload)
    )

def get_generic_token():
    endpoint = "https://accounts.spotify.com/api/token"
    method = urlfetch.POST
    headers =  {
        'Authorization': 'Basic ' + client_details
    }
    payload = {
        'grant_type': "client_credentials"
    }
    return make_request(endpoint, method, headers, urllib.urlencode(payload))

def get_user_data(access_token):
    endpoint = "https://api.spotify.com/v1/me"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + access_token
    }
    return make_request(
        endpoint,
        urlfetch.GET,
        headers
    )

def get_listens(access_token):
    endpoint = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + access_token
    }
    payload = {
        'limit': 50
    }
    return make_request(
        endpoint,
        urlfetch.GET,
        headers,
        urllib.urlencode(payload)
    )

def get_multi_track_features(id_list_string):
    token_obj = get_generic_token()
    if (token_obj == False): return False
    access_token = token_obj['access_token']
    endpoint = "https://api.spotify.com/v1/audio-features"
    method = urlfetch.GET
    headers = {
        'Authorization': "Bearer " + access_token
    }
    payload = {
        'ids': id_list_string
    }
    logging.info("Making request for ids: " + id_list_string)
    return make_request(endpoint, method, headers, urllib.urlencode(payload))
