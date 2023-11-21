# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 00:52:32 2021

@author: nicol
"""

import loading as load
import requests
import json

import authorization as au
import webbrowser

CONFIRMATION_CODE = 200 # Risposta di conferma affermativa dall'api spotify
ALTERNATIVE_CONFIRMATION_CODE = 201 # Risposta di conferma affermativa dall'api spotify

def post_thing(request_string, body, paths, params = {}, PARAMS = False):
    
    auth = load.get_oauth(paths)
    request_headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth}
    query_params = params
    
    if PARAMS:
        response = requests.post(request_string, headers = request_headers, data = body, params = query_params)
    else:
        response = requests.post(request_string, headers = request_headers, data = body)
    
    if response.status_code != CONFIRMATION_CODE and response.status_code != ALTERNATIVE_CONFIRMATION_CODE:   # Spesso questo problema c'è per l'oauth token scaduto
        print("C'è stato un problema con la richiesta (CODE: " + str(response.status_code) + "):\n" + response.text + "\nProvo a ripristinare l'OAUTH token? [0/(1)] ")
        risposta = input()
        if risposta == '0':
            raise ValueError("Interruione manuale in seguito ad errore in una richiesta.")
        au.refresh_access_token(paths)
        return post_thing(request_string, body, paths, params, PARAMS)   # Richiamo la funzione
    return response

def create_playlist(name, timestamp, uris, paths):
    
    user_id = load.get_user_id(paths)
    
    request_string = get_url_request(r'users/' + user_id + r'/playlists', '')
    description = timestamp + " - Playlist built through the software PORTAMENTO"
    body = "{\"name\":\"" + name + "\",\"description\":\"" + description + "\",\"public\":false}"
    
    response = post_thing(request_string, body, paths)
    response = json.loads(response.text)
    
    playlist_id = response['id']
    request_string = get_url_request(r'playlists', playlist_id + r'/tracks')
    body = "{\"uris\":" + uris + "}"
    response = post_thing(request_string, body, paths)
    
    return playlist_id

def get_url_request(req_type, req_id):
    
    # Crea l'url a cui fare la richiesta
    # esempio: req_type = audio-features , req_id = ids of the songs
    return r'https://api.spotify.com/v1/' + req_type + r'/' + req_id