# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 00:52:32 2021

@author: nicol
"""

import loading as load
import requests
import webbrowser

import authorization as au

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

def create_playlist(name, timestamp, paths):
    
    user_id = load.get_user_id(paths)
    request_string = get_url_request(r'users/' + user_id + r'/playlists', '')
    
    description = timestamp + " - Playlist built through the software PORTAMENTO"
    body = "{\"name\":\"" + name + "\",\"description\":\"" + description + "\",\"public\":false}"
    
    post_thing(request_string, body, paths)

def get_url_request(req_type, req_id):
    
    # Crea l'url a cui fare la richiesta
    # esempio: req_type = audio-features , req_id = ids of the songs
    return r'https://api.spotify.com/v1/' + req_type + r'/' + req_id


"""
if response.status_code != CONFIRMATION_CODE:   # Spesso questo problema c'è per l'oauth token scaduto
        print("C'è stato un problema con la richiesta (CODE: " + str(response.status_code) + "):\n" + response.text + "\nProva a vedere questo link per ottenere l'OAUTH token: \nhttps://developer.spotify.com/console/get-audio-analysis-track")
        webbrowser.open("https://developer.spotify.com/console/get-audio-analysis-track")
        auth = input("Inserisci l'OAUTH token: (scrivi stop se vuoi fermare qui l'esecuzione) ") # Rinnovo l'oauth token
        if auth == "stop" or auth == "STOP":
            raise ValueError("Oauth aveva il valore di stop del loop")
        oauth = open(paths.oauth, "w")        
        oauth.write(auth)
        oauth.close()
        print('\n')
"""