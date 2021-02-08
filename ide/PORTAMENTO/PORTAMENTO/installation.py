# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:32:16 2020

@author: nicol
"""
import paths_info as install
import os
import sys

def main(user = r'nic'):
    
    paths = install.Path(user)    # COSTRUISCO I PATH BASE
    paths.initialize_default_files()    # INIZIALIZZO I TABLES (QUESTO LI SOVRASCRIVE)
    
    return 0

#************************************************
def build_user_path(user):
    # COSTRUISCO IL PATH ROOT
    root = os.getcwd()
    root = root[:-26] # 26 PERCHE' QUESTO E' IL NUMERO DI CARATTERI DA CANCELLARE DATI DA "ide\PORTAMENTO\PORTAMENTO". DA RIACCORDARE SE SI CAMBIANO NOMI ALLE DIRECTORY
    
    # CREO IL PATH DELL'USER SE NON ESISTE GIA'
    user_path = os.path.join(root, r'users', user)
    if(not os.path.isdir(user_path)):
            os.mkdir(user_path)



if __name__=="__main__":
    main(sys.argv[1])
    #main()    # Per prove