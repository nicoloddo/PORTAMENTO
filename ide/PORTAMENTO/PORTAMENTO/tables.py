# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 11:41:09 2020

@author: nicol
"""

import pandas as pd
import json

class Tab:    # Le table sono dei dataframe in cui vi sono elencati i vari preset di: weights, datasets e axis
    
    def __init__(self, table_type_in, paths):
        
        self.table_type = table_type_in
        
        self.table = pd.read_csv(table_path(self.table_type, paths))    # Carico il dataframe
        self.table = self.table.set_index('id')
    
    
    def create(self, path):
        # in questa funzione devo pensare a caricare un file creato da unity con i nuovi parametri per la nuova riga della table, selezionati dall'utente dall'interfaccia
        # self.new = 
        pass
        
    def save(self, new):    # salvo la nuova riga
        # self.table = self.table.append(self.new, ignore_index = True)
        pass


    def get(self, preset_name):
        to_return = self.table.loc[preset_name].to_dict()
        
        if self.table_type == "weights":
            to_return = format_weight_preset(to_return)
        
        return to_return


def table_path(table, paths):
    
    if table == "weights":
        table_path = paths.weights_table
    elif table == "datasets":
        table_path = paths.datasets_table
    elif table == "axis":
        table_path = paths.axis_table
    else:
        raise ValueError("Table type invalido in Table.table_path")
            
    return table_path
        

def format_weight_preset(preset):   # mette in una forma utilizzabile meglio il preset weight.
    preset['weights'] = json.loads(preset['weights'])
    return preset


class Tables:
    
    def __init__(self, paths):
        
        self.weights = Tab("weights", paths)
        self.datasets = Tab("datasets", paths)
        self.axis = Tab("axis", paths)
    