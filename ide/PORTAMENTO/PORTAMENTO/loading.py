# PER RICEVERE I DATI SULLE CANZONI
import requests

import webbrowser

import authorization as au

CONFIRMATION_CODE = 200 # Risposta di conferma affermativa dall'api spotify
MAX_IDS_PER_REQUEST = 100 # Massimo numero di ids per feature request (imposto da spotify)
MAX_IDS_PLAYLIST_REQUEST = 100 # Massimo numero di items forniti dalla richiesta di una playlist

#************************************************************************************************************************************
def get_song_analysis(song_id, paths):   # In questa funzione faccio la richiesta della canzone e metto la struttura nella forma che interessa a me.

    return request_audio_analysis(song_id, paths)

#-------------
def get_playlist(playlist_id, paths):   # Gestisce la richiesta della playlist
    
    return request_playlist(playlist_id, paths)

#-------------
def get_features(songpack, paths, features, count = 0):   # Gestisce il limite di 100 id per richiesta e effettua la richiesta di features a gruppi
    
    if features == 'first':    # Prima chiamata
        features = []
        
    ids = "?ids="
    
    # mi segno il massimo che devo raggiungere
    max_count = count + MAX_IDS_PER_REQUEST
    
    # Creo il songpack di ids
    while count < len(songpack):
        song_id = songpack[count]['id']
        
        if count < max_count:
            ids = ids + song_id + ','
            count = count + 1
        else:   # Appena raggiungo il limite di ids
            # effettuo la richiesta con gli ids appena caricati 
            features.extend(request_features(ids, paths, count - MAX_IDS_PER_REQUEST)) # raccimolati i primi 100 ids, effettuo la richiesta per quelli (offset a 0), poi proseguo con i secondi 100 ids
            return get_features(songpack, paths, features, count)
        
    features.extend(request_features(ids, paths, count))
        
    return features
    
#************************************************************************************************************************************
def get_oauth(paths):
    
    oauth = open(paths.oauth, "r")  # Leggo il token di autenticazione  # Leggo il token di autenticazione
    auth = oauth.read()
    oauth.close()
    return auth

#************************************************************************************************************************************
def get_user_id(paths):
    
    url_request = get_url_request('me', '')
    response = request_thing(url_request, paths)
    user_id = response.json()['id']
    return user_id

#************************************************************************************************************************************
def get_url_request(req_type, req_id):
    
    # Crea l'url a cui fare la richiesta
    # esempio: req_type = audio-features , req_id = ids of the songs
    return r'https://api.spotify.com/v1/' + req_type + r'/' + req_id
    

#************************************************************************************************************************************
def request_thing(request_string, paths, offset = 100, PARAMS = False):
    
    auth = get_oauth(paths)
    request_headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth}
    query_params = {'offset' : offset}
    
    if PARAMS:
        response = requests.get(request_string, headers = request_headers, params = query_params)
    else:
        response = requests.get(request_string, headers = request_headers)
        
    if response.status_code != CONFIRMATION_CODE:   # Spesso questo problema c'è per l'oauth token scaduto
        print("C'è stato un problema con la richiesta (CODE: " + str(response.status_code) + "):\n" + response.text + "\nProvo a ripristinare l'OAUTH token? [0/(1)] ")
        risposta = input()
        if risposta == '0':
            raise ValueError("Interruione manuale in seguito ad errore in una richiesta.")
        au.refresh_access_token(paths)
        return request_thing(request_string, paths, offset, PARAMS)   # Richiamo la funzione
    return response
    
#-------------    
def request_features(ids, paths, offset):
     
    url_request = get_url_request('audio-features', ids)
    response = request_thing(url_request, paths, offset, True)
    features = response.json()['audio_features']
    return features

#-------------
def request_playlist(playlist_id, paths):

    url_request = get_url_request('playlists', playlist_id)
    response = request_thing(url_request, paths)
    playlist = response.json()
    
    num_songs = playlist['tracks']['total']
    items = get_items(playlist_id, num_songs, paths, 'first')
    playlist['tracks']['items'] = items
    return playlist

def get_items(playlist_id, num_songs, paths, items, count = 0):
    
    # ATTENZIONE: IL MODO IN CUI HO OTTENUTO IL CICLO DI OFFSET E' BEN DIVERSO DA QUELLO USATO NEL get_features POICHE' AVEVO ESIGENZE DIVERSE.
    if items == 'first':    # Prima chiamata
        items = []
    
    while count < num_songs:
        # richiedo e aggiorno la lista di items
        items.extend(request_items(playlist_id, paths, count))
        
        # richiamo la funzione per i prossimi 100
        return get_items(playlist_id, num_songs, paths, items, count + MAX_IDS_PLAYLIST_REQUEST)
    
    return items
    
def request_items(playlist_id, paths, offset):
    
    url_request = get_url_request('playlists', playlist_id) + r'/tracks'
    response = request_thing(url_request, paths, offset, True)
    items = response.json()['items']
    return items
    
#-------------
def request_audio_analysis(song_id, paths):
    
    url_request = get_url_request('audio-analysis', song_id)
    response = request_thing(url_request, paths)
    song = response.json()
    return song