# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:00:15 2021

@author: nicol
"""
import pandas as pd
import numpy as np

import paths_info
import pickle
from freediscovery.cluster import birch_hierarchy_wrapper

class Clusters_interface:
    
    def init(user):
        
        last_path = paths_info.Path(user).last_path    # Ottengo 

        paths = pd.read_csv(last_path)

        with open(paths.model[0], "rb") as file:
            model = pickle.load(file)
        
        
        
        