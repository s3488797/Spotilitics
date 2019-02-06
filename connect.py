import os
import urllib
import httplib, base64, json, logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import jinja2
import webapp2

CLIENT_ID = "4f2c1f999a4c480f9d9eea2f82b53723"
CLIENT_SECRET = "ba1c5975884d4ba080e84b8540b1bc6a"
PROJECT_ID = 's3488797-cc2019'
client_details = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
REDIRECT_URI = "https://" + PROJECT_ID + ".appspot.com/callback"
SCOPES = "user-read-private user-read-recently-played user-read-currently-playing"

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

# Generic method to make a HTML request
def make_request(endpoint, method, headers, payload=None):
    if (method == urlfetch.GET and payload != None):
        endpoint = endpoint + "?" + urllib.urlencode(payload)
    if (payload != None) :
        payload = urllib.urlencode(payload)
    fetch_results = urlfetch.fetch(
        url=endpoint,
        payload=payload,
        method=method,
        headers=headers
    )
    results = json.loads(fetch_results.content)
    if (fetch_results.status_code != 200):
        return results
        error_string = "Error occured making " + str(method) + " request"
        if (method == urlfetch.POST):
            error_string += ": " + str(results['error_description'])
        logging.error(error_string)
        return False
    return results

# Initial request for access of a user
def request_user_access(auth_code):
    endpoint = 'https://accounts.spotify.com/api/token'
    method = urlfetch.POST
    payload = {
        'grant_type': "authorization_code",
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Authorization': 'Basic ' + client_details
    }
    return make_request(endpoint, method, headers, payload)

def refresh_user_access(refresh_token):
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

def request_generic_access():
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
    method = urlfetch.GET
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + access_token
    }
    payload = {
        'limit': 50
    }
    return make_request(endpoint, method, headers, payload)

def get_listens_after(access_token, timestamp):
    endpoint = "https://api.spotify.com/v1/me/player/recently-played"
    method = urlfetch.GET
    headers = {
        'Authorization': "Bearer " + access_token,
        'Accept': "application/json",
        'Content-Type': "application/json"
    }
    payload = {
        'limit': 50,
        'after': timestamp
    }
    return make_request(endpoint, method, headers, payload)

# method for extracting the list of ids from a listen history set
def get_listens_id_list(listens):
    id_string_list = ""
    for track in listens['items']:
        id_string_list += track['track']['id'] + ","
    id_string_list = id_string_list[:-1]
    return id_string_list

def get_multi_track_features(listens):
    token_obj = request_generic_access()
    id_list_string = get_listens_id_list(listens)
    if (token_obj == False): return False
    access_token = token_obj['access_token']
    endpoint = "https://api.spotify.com/v1/audio-features"
    method = urlfetch.GET
    headers = {
        'Authorization': "Bearer " + access_token,
        'Accept': "application/json",
        'Content-Type': "application/json"
    }
    payload = {
        'ids': id_list_string
    }
    logging.info("Making request for ids: " + id_list_string)
    return make_request(endpoint, method, headers, payload)

def get_listens_album_id_list(listens):
    id_string_list = ""
    for track in listens['items']:
        id_string_list += track['track']['album']['id'] + ","
    id_string_list = id_string_list[:-1]
    return id_string_list

def get_multi_track_albums(listens):
    token_obj = request_generic_access()
    id_list_string = get_listens_album_id_list(listens)
    if (token_obj == False): return False
    access_token = token_obj['access_token']
    endpoint = "https://api.spotify.com/v1/albums"
    method = urlfetch.GET
    headers = {
        'Authorization': "Bearer " + access_token,
        'Accept': "application/json",
        'Content-Type': "application/json"
    }
    payload = {
        'ids': id_list_string
    }
    return make_request(endpoint, method, headers, payload)

def get_multi_track_genres(listens):
    albums = get_multi_track_albums(listens)
    listens_genres = []
    for album in albums['albums']:
        listens_genres += [album['genres']]
    return listens_genres
