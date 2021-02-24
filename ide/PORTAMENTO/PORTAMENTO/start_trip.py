# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:16:16 2021

@author: nicol
"""

import sys

import paths_info
import datasets_utils as dt

def main(bundle_name = "portamento", radar_name = "default", NEW_RADAR = True, user = "nic", CMD_LINE = True):
    '''!!!PRIMA DI UTILIZZARLO CONTROLLA IL NEW_RADAR!!! SE LO VUOI RISCARICARE DEVE ESSERE True, SE NO False.'''
    
    '''
    QUESTO SCRIPT SERVE A CREARE IL RADAR NEL CASO SIA NUOVO E A SALVARE DATASET E RADAR NEL LAST_PATH.
    E' SOSTANZIALMENTE UNA PREPARAZIONE A cluster_interface.py CHE USA IL LAST_PATH PER FORNIRE I CLUSTER ALL'INTERFACCIA.
    '''
    root = r'D:\PROJECTS\PORTAMENTO'
    
    paths = paths_info.Path(user, root)
    
    # COLLEGO DATASET E RADAR
    paths.link_database(bundle_name)
    paths.link_radar(radar_name)
    
    # CREO IL RADAR SE E' NUOVO
    if(NEW_RADAR):
        if(CMD_LINE):
            print("Inserisci l'uri della playlist di radar nel file creato in radars/, poi clicca invio. \n")
            input("Ricorda che non verranno visualizzate più di 12 canzoni come radar in ogni caso. \n")
        is_radar = True
        radar = dt.Dataset(paths, is_radar, NEW_RADAR)
        
    paths.pack_paths()
    
    return 0


if __name__=="__main__":
    #main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], False)
    main()    # Per avvio dall'ide