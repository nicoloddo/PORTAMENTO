# IMPORTO I PATHS
import paths_info as path

# IMPORTO DATASET UTILITIES
import datasets_utils as dt

#********************************* MAIN ******************************************************
def main():
    
    base_path = r'D:\PROJECTS\PORTAMENTO'
    bundle_name = "first_test"
    
       # r' '  serve ad evitare che python interpreti \t come un <tab> e tutte le altre cose dovute al backslash. Conviene sempre usarlo nei path
    percent_track_clust = 0.25  # Precisione della ricerca per track: quante canzoni dovrei mettere nello stesso gruppo rispetto a quante sono quelle totali
    percent_segm_clust = 0.25    # Precisione della ricerca per suoni: quanti suoni dovrei mettere nello stesso gruppo rispetto a quanti sono i totali 
    percent_sound_min = 0.3    # Percentuale di suoni di quel tipo devono esserci in una canzone per cui ci sia una somiglianza con un'altra. In termini di suoni/suoni_totali
    percent_sound_acc = 0.1  # Ogni quanti suoni tratti dall'analisi, possiamo considerare come un solo suono all'interno di una canzone? Se è 0.2 ad esempio, suoni totali * 1/5 significa che avremo un suono ogni 5 suoni analizzati
    track_min_confidence = 0.3    # minima accuratezza di uno dei vari parametri del risultato delle analisi di spotify per considerare la canzone
    segm_min_confidence = 0.1    # minima accuratezza del risultato delle analisi di spotify per considerare il suono.
        
    new_load = input("Nuovo caricamento? [0/1] - ")
        
    paths = path.Path(base_path, bundle_name)     # Costruisco i path base
        
    data = dt.Dataset(paths, new_load)
            
        
            
    # print ("\nAllenamento per la parte track...")
    # track_train(track_min_confidence, percent_track_clust, data['track'], paths)
    # dataset_tr = data['track']
        
    # print ("\nAllenamento per la parte segments...")
    # segments_train(segm_min_confidence, percent_segm_clust, percent_sound_min, data['segments'], paths, percent_sound_acc)
    # dataset_sg = data['segments']
    
    return 0

if __name__=="__main__":
    main()