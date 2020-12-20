# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 11:41:09 2020

@author: nicol
"""

class Weights:
    
    def __init__(self):
        
        self.weights = {}
    
    
    def crea(self, paths):
        # in questa funzione devo pensare a caricare un file creato da unity con weights selezionati dall'utente dall'interfaccia
        pass
        
    def save(self, name, description, weights_database):
        
        weights_database = weights_database.append(self.weights, ignore_index = True)
        
    
    def load(self, pack_name, weights_database):
        
        self.name = pack_name
        self.weights = weights_database.loc[pack_name]