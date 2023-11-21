import json
import sys

# IMPORTO I PATHS
import paths_info

# IMPORTO I TABLES
import tables as tb

# IMPORTO DATASET UTILITIES
import datasets_utils as dt

# IMPORTO LE UTILITIES DI CLUSTERING
import clustering as cl

#********************************* MAIN ******************************************************
def main(bundle_name = "mosiselecta", NEW_LOAD = False, SAVE_DATASET = True, SAVE_FINAL_CLUSTERS = False, SONG_ANALYSIS_BOOL = False, CMD_LINE = True, user = r'nic'):    
    
    '''   
    QUESTO SCRIPT SERVE A CLUSTERIZZARE UN DATASET QUALUNQUE CHE POI UTILIZZEREMO PER I CLUSTER DELL'INTERFACCIA.
    
    SAVE_FINAL_CLUSTERS :
        BOOL PER DECIDERE SE SALVARE I RISULTATI. NON FUNZIONA ORA PERCHE' SALVA I CLUSTER FOGLIA CHE SONO UN SACCO, NON SALVA QUELLI DEL PRIMO LIVELLO
    
    SONG_ANALYSIS_BOOL :
        BOOL PER DECIDERE SE FARE L'ANALISI APPROFONDITA O NO
        
    CMD_LINE:
        BOOL PER SAPERE SE LO STO AVVIANDO DA COMMAND_LINE O NO
    
    NEW_LOAD:
        BOOL PER SAPERE SE E' UN NUOVO CARICAMENTO O NO, SE L'AVVIAMENTO E' DA COMMAND LINE, VIENE CHIESTO DURANTE L'ESECUZIONE
    '''
    
    # PARAMETRI:   
    # parametri Birch
    birch_threshold = 0.2
    branch_factor = 18
    
    
    # ************* INIZIO
    root = r'D:\PROJECTS\PORTAMENTO'
    paths = paths_info.Path(user, root)    # COLLEGO I PATH ALLE MIE STRUTTURE
    
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
    paths.delete_saved_clusters(paths.track_final_clust)
    paths.delete_saved_clusters(paths.track_uri_clust)
    
    if new_load and CMD_LINE:
        input("Inserisci gli uri delle playlist nel file creato in bundles/" + bundle_name + ", poi clicca invio. \n")
    
    # Carico il dataset
    is_radar = False
    loaded = dt.Dataset(paths, is_radar, new_load, SAVE_DATASET, SONG_ANALYSIS_BOOL)
    data = loaded.dataset
    

    '''
    if CMD_LINE:
        input("Caricamento avvenuto, premi invio per avviare la clusterizzazione.\n")
    '''
    
    # Creo il clusterer       
    clust = cl.Clusterer(data, weights, SAVE_FINAL_CLUSTERS)
    # Avvio il clustering
    params = True    # se usare i parametri inseriti dall'utente o i default
    if params == True:
        clusters = clust.cluster_new_dataset(paths, birch_threshold, branch_factor) # in ingresso prende i parametri dell'algoritmo utilizzato
    else:
        clusters = clust.cluster_new_dataset(paths) # parametri di default
    
    
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
    
    root_in_inspector = clust.model.root_.subclusters_
    return 0

if __name__=="__main__":
    #main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], False)
    main()    # Per avvio dall'ide