# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 03:39:30 2020

@author: nicol
"""

def save_segm_clust(clusters, song_of_sound, song_lenght, n_songs, percent_min, dataset, paths):   # Funzione specifica per salvare i cluster dei segmenti. 
    # La complessità è anche qui pari al numero dei suoni, ossia la lunghezza del vettore labels, esattamente come in save_clusters. 
    # !! IMPORTANTE !! Questa funzione prende in ingresso la variabile dei clusters, non dei labels: bisogna prima eseguire save_clusters sui labels.
   
    #TODO: Passando dataset, potrebbe essere ridondante passare anche n_songs. Verifica
    song_clusters = []  # Questo sarà il nuovo cluster con all'interno canzoni anzichè suoni
    

    count_cluster = 0
    for cluster in clusters:
        song_clusters.append([])    # Inizializzo il primo cluster nella lista dei cluster per canzone
        salva = open(paths['segments_clust'] + r'\cluster' + str(count_cluster) + ".txt", "w+")   # apro il file dove salvare il cluster
        sounds_in = [0] * n_songs    # In sounds_in c'è un conteggio temporaneo di quanti suoni del cluster ci sono in ogni canzone. L'indice indica la canzone.
            
        for sound in cluster:
            song = song_of_sound[sound]
            if song not in song_clusters[count_cluster]:    # Controllo che non sia già nel cluster per evitare verifiche inutili
                sounds_in[song] = sounds_in[song] + 1    # Aggiungo uno alla canzone con quel suono
                percent = sounds_in[song] / song_lenght[song]    # Se la canzone supera come percentuale di quel suono quella minima stabilita, la salvo nel cluster
                
                if percent >= percent_min:
                    uri = dataset['uris'][song]   # leggo dalla sezione con gli uri.
                        
                    salva.write(uri)
                    
                    song_clusters[count_cluster].append(song)   # La aggiungo al cluster
                        
        count_cluster = count_cluster + 1     
        salva.close()
        
    return song_clusters


#************************************************************************************************************************************
def save_clusters(n_clusters, labels, dataset, paths, scope = 'error', save_in_file = 0):  # salva i clusters. Lo scope può essere: track, segments, sections.
        
    salva = []  # Vettore di puntatori a file per aprire tutti i file dove scrivo i clusters insieme
    clusters = []   # Vettore dove definisco la composizione dei clusters
    
    if scope != 'track' and scope != 'segments' and scope != 'sections':
        raise ValueError('Lo scope non è stato definito o è stato definito erroneamente')
        
    if save_in_file == 1:
        for i in range(n_clusters): # Inizializzazione dei vettori
             salva.append(open(paths[scope + '_clust'] + r'\cluster' + str(i) + ".txt", "w+"))
             clusters.append([])
             
        count = 0
        for uri in dataset['uris']:
            salva[labels[count]].write(uri)
            count = count + 1
        
        for i in range(n_clusters): # Chiudo i files
             salva[i].close()
    
    elif save_in_file == 0:
        for i in range(n_clusters): # Inizializzazione dei vettori
            clusters.append([])
    else:
        print("save_in_file non valido: deve essere un bool!")
    
    for i in range(labels.size):    # Compilo il vettore clusters
        clusters[labels[i]].append(i)
        
    print("\n**I clusters son stati salvati nella cartella!**  PATH: " + paths[scope + '_clust'])
    print("\nUSA QUESTO STRUMENTO PER VEDERE LE CANZONI IN UN CLUSTER:")
    print("https://www.spotlistr.com/search/textbox") 
    print("\nI risultati scarsi possono essere dovuti, oltre al numero basso di parametri utilizzati, al fatto che non sto ancora considerando l'accuracy dei parametri  le canzoni.")
    
    return clusters


#************************************************************************************************************************************
def filtra(min_confidence, general_dataset, scope, paths, printa = 1, i = -1):    # Filtra i parametri inseriti nella blacklist e suoni o canzoni con bassa accuratezza di analisi.
    
    if scope == 'track':
        dataset = general_dataset[scope]
        conf = general_dataset[scope + '_confidences']
    else:
        dataset = general_dataset[scope][i]
        conf = general_dataset[scope + '_confidences'][i]

    
    # FILTRO PARAMETRI:
    nome_blacklist = chr(92) + scope + '_blacklist'    # chr(92) sarebbe '\'
    if printa == 1:
        print("\nSto filtrando questi parametri da " + scope + ": ")
    
    with open(paths['black'] + nome_blacklist + ".txt", "r") as blacklist:   #Filtro i parametri della clusterizzazione di track.
        for thing in blacklist:
            if 'FINE' in thing:
                break
            thing = thing[:-1]  # Tolgo l'ultimo carattere che sarà o un \n o un carattere EOF
            if printa == 1:
                print(thing)
            try:
                dataset = dataset.drop(thing, axis = 1)   # Cancella colonne in pandas
                if scope == 'track':    # Tolgo quei parametri anche dalle confidence. Lo faccio solo per track perchè segments ha un solo parametro di confidenza generale. Potrebbe valere la stessa cosa per sections
                    conf = conf.drop(thing + '_confidence', axis = 1)
            except ValueError:
                assert False, "ERRORE!!! - La blacklist contenuta nella cartella della playlist non è valida! Ricorda che i parametri vanno uno per riga e che non possono essere le confidenze stesse."
    
    if printa == 1:
        print('\n')
        
    #FILTRO CANZONI (O SUONI NEL CASO DI SEGMENTS E SECTIONS):
    delete = []
    stats = {key:0 for key in dict(conf)}   
                
    for index, row in conf.iterrows():    # trovo le righe del dataset che hanno parametri con accuratezza bassa. Le righe possono essere le canzoni stesse oppure i suoni, se stiamo filtrando segments
        already = 0
        row = dict(row)
        for key in row:
            if row[key] < min_confidence:
                if already == 0:
                    delete.append(index)    # aggiungo quella riga a quelle da cancellare
                    already = 1
                stats[key] = stats[key] + 1     # Mi segno statistiche su quali parametri per lo più erano di accuratezza bassa
    
    for index in sorted(delete, reverse = True):    # E' importante che la lista sia al contrario (reverse = true) perchè se elimino cose all'inizio, tutti gli indici scalano e io sbaglio cosa cancellare
        dataset = dataset.drop(index)     # cancello la riga
        if scope == 'track':    #  Lo faccio solo per track perchè in segm e sect cancello suoni e non canzoni!
            del general_dataset['uris'][index]      # tolgo la canzone dagli uri.
            general_dataset['n_songs'] = general_dataset['n_songs'] - 1
    
    if scope == 'track':
        general_dataset[scope] = dataset       # Aggiorno il dataset
    else:
        general_dataset[scope][i] = dataset
    
    return stats


#************************************************************************************************************************************
def track_train(min_confidence, percent_clust, dataset, paths):    # Clusterizzazione del track
     
    old_tot_parameters = dataset['track'].shape[1]
    old_tot_songs = dataset['n_songs']
    # MATRICE A PUNTINI IN 2D 
#    scatter_matrix(track)
#    plt.show()
    
    stats = filtra(min_confidence, dataset, 'track', paths)    # Filtro il dataset track    
    track = dataset['track']    # Caricamento del dataset track
    
    print('Canzoni: ' + str(dataset['n_songs']) + '/' + str(old_tot_songs) + '  -->  ' + str(old_tot_songs - dataset['n_songs']) + " cancellate")
    print('Parametri considerati: ' + str(track.shape[1]) + '/' + str(old_tot_parameters) + '  -->  ' + str(old_tot_parameters - track.shape[1]) + " cancellati")
    
    print("\nStatistiche delle canzoni: quante erano sotto il minimo di confidenza nei parametri dell'analisi di spotify. (Ci possono essere canzoni che son sotto per più di un parametro)")
    for key in stats:
        print(str(stats[key]) + ' - ' + key)
    
    n_clusters = int(track.shape[0] * percent_clust)
    
    array = track.values  # trasformo in lineare. dovrei usare il metodo .to_numpy() in realtà: values verrà deprecato. Però non ho ancora aggiornato pandas
    
    # 0 : Metodo kmeans; 1 : AgglomerativeClustering
    scelta = 1
    
    if scelta == 0:
        kmeans = KMeans(n_clusters=n_clusters)  # Creo innanzitutto la variabile del metodo
        distances = kmeans.fit_transform(array) # Applico kmeans all'array lineare. Questa è tutta la parte di clustering e riconoscimento.
        centroids = kmeans.cluster_centers_    # Estraggo cluster_centers dalla clusterizzazione
        labels = kmeans.labels_   # Estraggo il vettore che indica in quale cluster è finita ogni canzone.
        
#        plt.scatter(array[:, 0], array[:, 1], c=labels, cmap='viridis');
#        plt.show()
    
    elif scelta == 1:
        ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        ward.fit(array)
        labels = ward.labels_
    
    clusters = save_clusters(n_clusters, labels, dataset, paths, 'track', save_in_file = 1)
    
    print("\nClusters: ")
    for count, cluster in enumerate(clusters):
        print(str(count) + '. ' + str(len(cluster)) + " Elementi")
    
    if scelta == 0:
        pack = {'track':track, 'clusters':clusters, 'labels':labels, 'distances':distances, 'centroids':centroids, 'n_songs' : track.shape[0]}
    elif scelta == 1:
        pack = {'track':track, 'clusters':clusters, 'labels':labels, 'n_songs':track.shape[0]}
    return pack


#************************************************************************************************************************************
def song_train(i, min_confidence, percent_sound, scope, dataset):
    pack = {'dataset':0, 'stats':0, 'del':0}
    
    if i == 0:
        printa = 1
    else:
        printa = 0
    
    old_n_sounds = dataset[scope][i].shape[0]   # Mi segno il numero di suoni prima del filtro    
    stats = filtra(min_confidence, dataset, scope, paths, printa, i)  
    song = dataset[scope][i]    # assegno la canzone
    if old_n_sounds / song.shape[0]  <  0.5:    # Se son stati cancellati troppi suoni per inaccuratezza, la canzone non è considerabile e la escludiamo
        pack['del'] = 1     # Uso questo parametro per segnalare che è da cancellare
        return pack
    
    
    # INIZIO LA CLUSTERIZZAZIONE PER IL RAGGRUPPAMENTO DI SUONI NELLA CANZONE
    n_clust = int(song.shape[0] * percent_sound)
    
    transp = song.T    # .T per transporre, questo per via di come il metodo prende gli argomenti
    array = transp.values    # trasformo in lineare. dovrei usare il metodo .to_numpy() in realtà: values verrà deprecato. Però non ho ancora aggiornato pandas
    method = FeatureAgglomeration(n_clusters=n_clust, linkage='ward') # Creo innanzitutto la variabile del metodo
    method.fit(array)
    song = method.transform(array)  # La canzone è ora compressa nel senso che son diminuiti i suoni che la componevano
    
#    labels = method.labels_
    
    song = pd.DataFrame(song)   # Ricreo un dataset con quei dati
    song = song.T    # Lo ritraspongo
    
    pack['dataset'] = song
    pack['stats'] = stats
    return pack
    
#************************************************************************************************************************************
def segments_train(min_confidence, percent_segm_clust, percent_min, dataset, paths, percent_sound_acc = 0.05):
    n_songs = dataset['n_songs']
    stats = {}
    delete = []     # Lista con tutte le canzoni da eliminare per indice
    
    segments = []   # Dataset con tutti i segmenti
    song_lenght = []    # Vettore con il numero di segmenti in ogni canzone
    song_of_sound = []  # Vettore con la canzone per ogni segmento (l'indice indica il segmento)
    
    for i, song in enumerate(dataset['segments']):
        pack = song_train(i, min_confidence, percent_sound_acc, 'segments', dataset) # Eseguo una "compressione" facendo un clustering dei suoni nella canzone
        stats = {key: stats.get(key, 0) + pack['stats'].get(key, 0) for key in set(stats) | set(pack['stats'])}     # aggiorno le statistiche
        song = pack['dataset']  # aggiorno la canzone
        # Note that set(dict1) | set(dict2) is the set of the keys of both your dictionaries. and dict1.get(key, 0) returns dict1[key] if the key exists, 0 otherwise.
        # https://stackoverflow.com/questions/45713887/add-values-from-two-dictionaries
        
        if pack['del'] == 0:
            segments.append(song)   # Aggiungo tutti i suoni della canzone al dataset dei segmenti
            
            for j in range(song.shape[0]):
                song_of_sound.append(i)    # Mi segno in questo vettore, a che canzone appartiene ogni suono per poi poter usare gli indici per ritrovarla.
        
            song_lenght.append(len(segments[i])) # Mi segno in song_lenght il numero di segmenti che appartengono alla canzone
        
        if pack['del'] == 1:
            delete.append(i)
    
    # CANCELLO LE CANZONI DA ELIMINARE DAGLI URI
    for index in sorted(delete, reverse = True):    # E' importante che la lista sia al contrario (reverse = true) perchè se elimino cose all'inizio, tutti gli indici scalano e io sbaglio cosa cancellare           
        n_songs = n_songs - 1
        del dataset['uris'][index]
        
    segments = pd.concat(segments)  # Carico tutti i segmenti delle canzoni e li metto insieme nello stesso dataset
    
    print("Statistiche dei suoni: quanti erano sotto il minimo di confidenza nei parametri dell'analisi di spotify. (Ci possono essere suoni che son sotto per più di un parametro)")
    for key in stats:
        print(str(stats[key]) + ' - ' + key)
    
    # CHECK NON PER FORZA NECESSARIA: TOGLIERE PER ALLEGGERIRE ----------------------------
    total_sounds = 0
    for i in range(n_songs):
        total_sounds = total_sounds + song_lenght[i]
    assert total_sounds == segments.shape[0], "Qualcosa è andato storto nel segments train."
    # FINE CHECK

    n_clusters = int(n_songs * percent_segm_clust)    # Calcolo numero di clusters
    print("\nNumero suoni totali: " + str(segments.shape[0]))
    print("Parametri a definire un suono: " + str(segments.shape[1]))
    print("Numero Clusters Voluti: " + str(n_clusters))
    
    # INIZIO LA CLUSTERIZZAZIONE DEI SUONI
    array = segments.values  # trasformo in lineare. dovrei usare il metodo .to_numpy() in realtà: values verrà deprecato. Però non ho ancora aggiornato pandas
#    kmeans = KMeans(n_clusters = n_clusters)  # Creo innanzitutto la variabile del metodo
#    distances = kmeans.fit_transform(array) # Applico kmeans all'array lineare. Questa è tutta la parte di clustering e riconoscimento.
#    centroids = kmeans.cluster_centers_    # Estraggo cluster_centers dalla clusterizzazione
#    labels = kmeans.labels_   # Estraggo il vettore che indica in quale cluster è finita ogni canzone.
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward.fit(array)
    labels = ward.labels_
    
    # Calcolo i clusters
    clusters = save_clusters(n_clusters, labels, dataset, paths, 'segments')
    clusters = save_segm_clust(clusters, song_of_sound, song_lenght, n_songs, percent_min, dataset, paths)
    
    # Stampo il numero di Clusters
    print("\nClusters: ")
    for count, cluster in enumerate(clusters):
        print(str(count) + '. ' + str(len(cluster)) + " Elementi")
    
    
    pack = {'segments':segments, 'song_from_sound':song_lenght, 'clusters':clusters, 'centroids':n_clusters, 'labels':labels}
    return pack