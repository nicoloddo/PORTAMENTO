# IMPORTO I PATHS
import paths_info as path

# PER RICEVERE I DATI SULLE CANZONI
import requests

CONFIRMATION_CODE = 200 # Risposta di conferma affermativa dall'api spotify

#************************************************************************************************************************************
def get_song_analysis(song_id, paths):   # In questa funzione faccio la richiesta della canzone e metto la struttura nella forma che interessa a me.
    
    #TODO: togliere la richiesta delle feature per metterne una sola tutta insieme
    
    oauth = open(paths.oauth, "r")  # Leggo il token di autenticazione  # Leggo il token di autenticazione
    auth = oauth.read()
    oauth.close()
    
    # Ottengo analisi da Spotify
    song_response = requests.get('https://api.spotify.com/v1/audio-analysis/' + song_id, headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth})
    if song_response.status_code != CONFIRMATION_CODE:
        print("C'è stato un problema con la richiesta: \n" + song_response.text + "\nProva a vedere questo link per ottenere l'OAUTH token: \nhttps://developer.spotify.com/console/get-audio-analysis-track")
        auth = input("Inserisci l'OAUTH token: ") # Rinnovo l'oauth token
        oauth = open(paths.oauth, "w")        
        oauth.write(auth)
        oauth.close()
        print('\n')
        return get_song_analysis(song_id, paths)   # Richiamo la funzione
        
    # Trasformo in json
    song = song_response.json()
    
    # Aggiungo song features
    song_response = requests.get('https://api.spotify.com/v1/audio-features/' + song_id, headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth})
    if song_response.status_code != CONFIRMATION_CODE:
        print("C'è stato un problema con la richiesta: \n" + song_response.text + "\nProva a vedere questo link per ottenere l'OAUTH token [CTRL+SHIFT+C]: \nhttps://developer.spotify.com/console/get-audio-analysis-track")
        auth = input("Inserisci l'OAUTH token: ") # Rinnovo l'oauth token
        oauth = open(paths.oauth, "w")        
        oauth.write(auth)
        oauth.close()
        print('\n')
        return get_song_analysis(song_id, paths)   # Richiamo la funzione
    
    song['track'].update(song_response.json())	# Aggiungo le features alla sezione track
    
    format_song(song)   # Formatto
    
    return song


def get_songpack(playlist_id, paths):
    
    oauth = open(paths.oauth, "r")  # Leggo il token di autenticazione
    auth = oauth.read()
    oauth.close()
    
    # Ottengo playlist da spotify
    response = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id, headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth})
    if response.status_code != CONFIRMATION_CODE:
        print("C'è stato un problema con la richiesta: \n" + response.text + "\nProva a vedere questo link per ottenere l'OAUTH token: \nhttps://developer.spotify.com/console/get-audio-analysis-track")
        auth = input("Inserisci l'OAUTH token: ") # Rinnovo l'oauth token
        oauth = open(paths.oauth, "w")
        oauth.write(auth)
        oauth.close()
        print('\n')
        return get_songpack(playlist_id, paths)   # Richiamo la funzione
    
    songpack = format_songpack(response.json())
    
    return songpack

def get_features(songpack, paths):
    
    oauth = oauth = open(paths.oauth, "r")  # Leggo il token di autenticazione  # Leggo il token di autenticazione
    auth = oauth.read()
    oauth.close()
    
    ids = "?ids="
    
    count = 0
    for song_id in songpack:
        if count <= 100:
            ids = ids + song_id + ','
            count = count + 1
        
    response = requests.get('https://api.spotify.com/v1/audio-features/' + ids, headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + auth})
    if response.status_code != CONFIRMATION_CODE:
        print("C'è stato un problema con la richiesta: \n" + response.text + "\nProva a vedere questo link per ottenere l'OAUTH token: \nhttps://developer.spotify.com/console/get-audio-analysis-track")
        auth = input("Inserisci l'OAUTH token: ") # Rinnovo l'oauth token
        oauth = open(paths.oauth, "w")        
        oauth.write(auth)
        oauth.close()
        print('\n')
        return get_features(songpack, paths)   # Richiamo la funzione
    
    features = response.json()['audio_features']
    
    format_features(features)
    
    return features
    
#************************************************************************************************************************************
def format_song(song):
    
    #TODO: Rimuovere la formattazione delle feature, poichè la farò sull'intero dataset con un format_dataset
    
    # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
    del song['track']['codestring']
    del song['track']['synchstring']
    del song['track']['rhythmstring']
    del song['track']['echoprintstring']
    del song['track']['track_href']
    del song['track']['id']
    del song['track']['type']
    del song['track']['analysis_url']
    del song['track']['sample_md5']
    del song['track']['window_seconds']
    del song['track']['synch_version']
    del song['track']['rhythm_version']
    del song['track']['echoprint_version']
    del song['track']['analysis_sample_rate']
    del song['track']['code_version']
    del song['track']['analysis_channels']
    del song['track']['offset_seconds']

    del song['track']['duration']
    del song['track']['num_samples']
    del song['track']['end_of_fade_in']
    del song['track']['start_of_fade_out']
    
    del song['track']['uri']    # Questi tanto li aggiungo al load del dataset direttamente dal songpack

    del song['meta']
    del song['bars']
    del song['beats']
    del song['tatums']

    for segment in song['segments']:
        del segment['start']
     
        # Rendo lineari i segmenti
    for segment in song['segments']:
        for i in range(len(segment['pitches'])):
            segment['pitch' + str(i)] = segment['pitches'][i]
        del segment['pitches']
        for i in range(len(segment['timbre'])):
            segment['timbre' + str(i)] = segment['timbre'][i]
        del segment['timbre']
    
    
    # SEPARO LE CONFIDENZE DAI VALORI
        
        # SECTIONS:
    song['sections_confidences'] = []
    count = 0
    for section in song['sections']:
        song['sections_confidences'].append({key:section[key] for key in section if 'confidence' in key})
        song['sections'][count] = {key:section[key] for key in section if 'confidence' not in key}
        count = count + 1
    
        # SEGMENTS:
    song['segments_confidences'] = []
    count = 0
    for segment in song['segments']:
        song['segments_confidences'].append({key:segment[key] for key in segment if 'confidence' in key})
        song['segments'][count] = {key:segment[key] for key in segment if 'confidence' not in key}
        count = count + 1

    # Avremo diviso ora il dizionario song in 4 keys: Track con informazioni generali sul sound della traccia, Segments con informazioni 
    # precise sui singoli suoni della traccia, Sections con informazioni sul sound di sezioni più grosse della traccia.
    # Avremo dunque 3 scope di precisione diversa.
    # C'è inoltre la key dell'ID in cui c'è semplicemente l'identificativo della traccia, che può essere visto come la precisione massima
    

def format_songpack(songpack):
    
    # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
    
    del songpack['collaborative']
    del songpack['external_urls']
    del songpack['followers']
    del songpack['href']
    del songpack['id']
    del songpack['images']
    del songpack['owner']
    del songpack['public']
    del songpack['snapshot_id']
    del songpack['type']
    del songpack['uri']
    

def format_features(features):
    
    # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
    for song in features:
    
        del song['track']['duration_ms']
        del song['track']['type']
        del song['track']['analysis_url']
        del song['track']['id']
        del song['track']['uri']    # Questi tanto li aggiungo al load del dataset direttamente dal songpack
        
        # SEPARO LE CONFIDENZE DAI VALORI
            # TRACK:
        song['track_confidences'] = {key:song['track'][key] for key in song['track'] if 'confidence' in key}
        song['track'] = {key:song['track'][key] for key in song['track'] if 'confidence' not in key}