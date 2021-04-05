# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 02:04:44 2021

@author: nicol
"""

import requests
import webbrowser
import json

import paths_info

from my_secrets import client_secret

CONFIRMATION_CODE = 200 # Risposta di conferma affermativa dall'api spotify
redirect_uri = 'http://linktr.ee/PERRERAHH'

def main(user = r'nic'):
    
    root = r'D:\PROJECTS\PORTAMENTO'
    paths = paths_info.Path(user, root)    # COLLEGO I PATH ALLE MIE STRUTTURE
    
    response = request_auth()
    webbrowser.open(response.url)
    temp_auth = input("Nell'URL a cui sarai reindirizzato dopo aver approvato l'accesso a Spotify, ci sarà scritto <code = ...> devi copiare tutto ciò che è scritto dopo l'uguale e incollarlo qui. Poi clicca invio.\n\n")
    
    response = request_tokens(temp_auth)
    
    if response.status_code != CONFIRMATION_CODE:   # Spesso questo problema c'è per l'oauth token scaduto
        print("C'è stato un problema con la richiesta (CODE: " + str(response.status_code) + "):\n" + response.text)
        
    response = json.loads(response.text)
          
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    
    salva = open(paths.oauth, "w")        
    salva.write(access_token)
    salva.close()
    
    salva = open(paths.refresh_token, "w")        
    salva.write(refresh_token)
    salva.close()

def request_auth():
    
    request_string = "https://accounts.spotify.com/authorize"
    query_params = {'client_id' : 'e6971699b1de430f8161d4093d1d0d09', 'response_type' : 'code', 'scope' : 'playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative', 'redirect_uri' : redirect_uri}
    
    response = requests.get(request_string, params = query_params)

    return response

def request_tokens(auth):
    
    request_string = "https://accounts.spotify.com/api/token"
    body = {'grant_type' : 'authorization_code', 'code' : auth, 'redirect_uri' : redirect_uri, 'client_id' : 'e6971699b1de430f8161d4093d1d0d09', 'client_secret' : client_secret}
    
    response = requests.post(request_string, data = body)
    
    return response

def refresh_access_token(paths):
    
    carica = open(paths.refresh_token, "r")  # Leggo il token di autenticazione  # Leggo il token di autenticazione
    refresh_token = carica.read()
    
    request_string = "https://accounts.spotify.com/api/token"
    body = {'grant_type' : 'refresh_token', 'refresh_token' : refresh_token, 'client_id' : 'e6971699b1de430f8161d4093d1d0d09', 'client_secret' : client_secret}
    
    response = requests.post(request_string, data = body)
    
    if response.status_code != CONFIRMATION_CODE:   # Spesso questo problema c'è per l'oauth token scaduto
        print("C'è stato un problema con la richiesta (CODE: " + str(response.status_code) + "):\n" + response.text)
        
    response = json.loads(response.text)
    access_token = response['access_token']
    
    salva = open(paths.oauth, "w")        
    salva.write(access_token)
    salva.close()

if __name__=="__main__":
    main()    # Per avvio dall'ide