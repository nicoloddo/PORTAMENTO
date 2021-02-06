import json

# IMPORTO I PATHS
import paths_info

# IMPORTO I TABLES
import tables as tb

# IMPORTO DATASET UTILITIES
import datasets_utils as dt

# IMPORTO LE UTILITIES DI CLUSTERING
import clustering as cl

#********************************* MAIN ******************************************************
def main():
    
    ''' QUESTA E' ROBA CHE SERVIVA IN SPOTIWORLD PER USARE SECTIONS E SEGMENTS:
    # r' '  serve ad evitare che python interpreti \t come un <tab> e tutte le altre cose dovute al backslash. Conviene sempre usarlo nei path
    percent_track_clust = 0.25  # Precisione della ricerca per track: quante canzoni dovrei mettere nello stesso gruppo rispetto a quante sono quelle totali
    percent_segm_clust = 0.25    # Precisione della ricerca per suoni: quanti suoni dovrei mettere nello stesso gruppo rispetto a quanti sono i totali 
    percent_sound_min = 0.3    # Percentuale di suoni di quel tipo devono esserci in una canzone per cui ci sia una somiglianza con un'altra. In termini di suoni/suoni_totali
    percent_sound_acc = 0.1  # Ogni quanti suoni tratti dall'analisi, possiamo considerare come un solo suono all'interno di una canzone? Se è 0.2 ad esempio, suoni totali * 1/5 significa che avremo un suono ogni 5 suoni analizzati
    track_min_confidence = 0.3    # minima accuratezza di uno dei vari parametri del risultato delle analisi di spotify per considerare la canzone
    segm_min_confidence = 0.1    # minima accuratezza del risultato delle analisi di spotify per considerare il suono.
    '''    
    
    user = r'nic'
    bundle_name = "sounds_of_everything"
    
    SONG_ANALYSIS_BOOL = False    # BOOL PER DECIDERE SE FARE L'ANALISI APPROFONDITA O NO
    CMD_LINE = True    # BOOL PER SAPERE SE LO STO AVVIANDO DA COMMAND_LINE O NO, SARA' PROBABILMENTE NEI PARAMETRI DI AVVIAMENTO DELLO SCRIPT
    NEW_LOAD = False
    
    # PARAMETRI:
    # parametri Kmeans:
    n_clusters_kmeans = 30    
    # parametri Birch
    n_clusters_birch = None
    threshold = 0.5
    branch_fact = 50
    
    paths = paths_info.Path(user)    # COLLEGO I PATH ALLE MIE STRUTTURE
    
    # IMPORTO LE SETTINGS
    with open(paths.settings, 'r') as settings:
        settings = json.load(settings)
    
    # IMPORTO I TABLES
    tables = tb.Tables(paths)
    # OTTENGO I WEIGHTS PER LA CLUSTERIZZAZIONE
    weights = tables.weights.get(settings["weights"])
    
    if CMD_LINE:
        print("Ricorda che se non hai mai fatto il caricamento comprensivo d'analisi, se ora volessi caricare il set con l'analisi, darebbe errori: in quel caso scegli di fare un nuovo caricamento.")
        new_load = input("Nuovo caricamento? [(0)/1] - ")

        if new_load == '1':
            new_load = True
        else:
            new_load = False
    else:
        new_load = NEW_LOAD
    
    # Collego o creo i path del database da caricare o creare
    paths.link_database(bundle_name)
    paths.delete_saved_clusters(paths.track_clust)
    paths.delete_saved_clusters(paths.track_uri_clust)
    
    if new_load:
        input("Inserisci gli uri delle playlist nel file creato in bundles/" + bundle_name + ", poi clicca invio. \n")
    
    # Carico il dataset
    loaded = dt.Dataset(paths, new_load, SONG_ANALYSIS_BOOL)
    data = loaded.dataset
    


    if CMD_LINE:
        input("Caricamento avvenuto, premi invio per avviare la clusterizzazione.\n")
    
    # Creo il clusterer       
    clust = cl.Clusterer(data, weights)
    # Avvio il clustering
    params = False    # se usare i parametri inseriti dall'utente o i default
    if params == True:
        clusters = clust.cluster_new_dataset(paths, n_clusters_kmeans, n_clusters_birch, threshold, branch_fact) # in ingresso prende i parametri dell'algoritmo utilizzato
    else:
        clusters = clust.cluster_new_dataset(paths) # parametri di default
    
    
    paths.pack_paths()
    
    # QUESTA PARTE E' ESCLUSIVAMENTE DEDICATA ALLA VISUALIZZAZIONE NELL'INSPECTOR
    filtered_clusters = []
    
    
    # filtro i cluster con le informazioni interessanti di clusterizzazione per visualizzarli bene nell'inspector
    relevant_columns = ['id', 'name']
    relevant_columns.extend(clust.audio_relevant_columns)
    for cluster in clusters:
        filtered_clusters.append(cluster[relevant_columns])
        
    
    # VECCHIA PARTE DEL CLUSTERING DEL MAIN
    # print ("\nAllenamento per la parte track...")
    # track_train(track_min_confidence, percent_track_clust, data['track'], paths)
    # dataset_tr = data['track']
        
    # print ("\nAllenamento per la parte segments...")
    # segments_train(segm_min_confidence, percent_segm_clust, percent_sound_min, data['segments'], paths, percent_sound_acc)
    # dataset_sg = data['segments']
    
    return 0

if __name__=="__main__":
    main()