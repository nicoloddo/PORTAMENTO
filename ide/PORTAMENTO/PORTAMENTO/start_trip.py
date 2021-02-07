# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:16:16 2021

@author: nicol
"""

import path_info
import datasets_utils as dt

def main(user = "nic", bundle_name = "sounds_of_everything", radar_name = "default", new_radar = True):
    
    paths = path_info.Path(user)
    
    # CREO IL RADAR
    if(new_radar):
        radar = dt.Dataset(paths, is_radar = True, new_radar)
    
    # COLLEGO DATASET E RADAR
    paths.link_database(bundle_name)
    paths.link_radar(radar_name)
    
        
    
    
    return 0


if __name__=="__main__":
    main()