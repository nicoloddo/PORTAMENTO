# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:16:16 2021

@author: nicol
"""

import paths_info
import datasets_utils as dt

def main(user = "nic", bundle_name = "sounds_of_everything", radar_name = "default", new_radar = True, CMD_LINE = False):
    '''
    QUESTO SCRIPT SERVE A CREARE IL RADAR NEL CASO SIA NUOVO E A SALVARE DATASET E RADAR NEL LAST_PATH.
    E' SOSTANZIALMENTE UNA PREPARAZIONE A cluster_interface.py CHE USA IL LAST_PATH PER FORNIRE I CLUSTER ALL'INTERFACCIA.
    '''
     
    paths = paths_info.Path(user)
    
    # COLLEGO DATASET E RADAR
    paths.link_database(bundle_name)
    paths.link_radar(radar_name)
    
    # CREO IL RADAR SE E' NUOVO
    if(new_radar):
        if(CMD_LINE):
            print("Inserisci l'uri della playlist di radar nel file creato in radars/, poi clicca invio. \n")
            input("Ricorda che non verranno visualizzate più di 10 canzoni come radar in ogni caso. \n")
        is_radar = True
        radar = dt.Dataset(paths, is_radar, new_radar)
        
    paths.pack_paths()
    
    return 0


if __name__=="__main__":
    main()