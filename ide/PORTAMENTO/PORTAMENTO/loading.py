# PER RICEVERE I DATI SULLE CANZONI
import requests

CONFIRMATION_CODE = 200 # Risposta di conferma affermativa dall'api spotify
MAX_IDS_PER_REQUEST = 100 # Massimo numero di ids per feature request (imposto da spotify)

#************************************************************************************************************************************
def get_song_analysis(song_id, paths):   # In questa funzione faccio la richiesta della canzone e metto la struttura nella forma che interessa a me.

    return request_audio_analysis(song_id, paths)

#-------------
def get_playlist(playlist_id, paths):   # Gestisce la richiesta della playlist
    
    return request_playlist(playlist_id, paths)

#-------------
def get_features(songpack, paths, count = 0):   # Gestisce il limite di 100 id per richiesta e effettua la richiesta di features a gruppi
    
    # TODO: IN QUESTO MOMENTO NON HA SENSO CREDO, RIPETE I PRIMI 100 ID PER SEMPRE

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
            features = request_features(ids, paths)
            return get_features(songpack, paths, count)
        
    features = request_features(ids, paths)
        
    return features
    
#************************************************************************************************************************************
def get_oauth(paths):
    
    oauth = oauth = open(paths.oauth, "r")  # Leggo il token di autenticazione  # Leggo il token di autenticazione
    auth = oauth.read()
    oauth.close()
    return auth

#************************************************************************************************************************************
def get_url_request(req_type, req_id):
    
    # Crea l'url a cui fare la richiesta
    # esempio: req_type = audio-features , req_id = ids of the songs
    return r'https://api.spotify.com/v1/' + req_type + r'/' + req_id
    

#************************************************************************************************************************************
def request_thing(request_string, paths):
    
    auth = get_oauth(paths)
    request_headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth}
    
    response = requests.get(request_string, headers = request_headers)
    if response.status_code != CONFIRMATION_CODE:   # Spesso questo problema c'è per l'oauth token scaduto
        print("C'è stato un problema con la richiesta (CODE: " + str(response.status_code) + "):\n" + response.text + "\nProva a vedere questo link per ottenere l'OAUTH token: \nhttps://developer.spotify.com/console/get-audio-analysis-track")
        auth = input("Inserisci l'OAUTH token: ") # Rinnovo l'oauth token
        if auth == "stop" or auth == "STOP":
            return "Fermato il loop dell'oauth"
        oauth = open(paths.oauth, "w")        
        oauth.write(auth)
        oauth.close()
        print('\n')
        return request_thing(request_string, paths)   # Richiamo la funzione
    return response
    
#-------------    
def request_features(ids, paths):
    
    url_request = get_url_request('audio-features', ids)
    response = request_thing(url_request, paths)
    features = response.json()['audio_features']
    return features

#-------------
def request_playlist(playlist_id, paths):
    
    url_request = get_url_request('playlists', playlist_id)
    response = request_thing(url_request, paths)
    playlist = response.json()
    return playlist

#-------------
def request_audio_analysis(song_id, paths):
    
    url_request = get_url_request('audio-analysis', song_id)
    response = request_thing(url_request, paths)
    song = response.json()
    return song