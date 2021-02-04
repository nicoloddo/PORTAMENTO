# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:32:16 2020

@author: nicol
"""
import paths_info as install

def main():
    
    user = r'nic'
    paths = install.Path(user)    # COSTRUISCO I PATH BASE
    paths.initialize_default_files()    # INIZIALIZZO I TABLES (QUESTO LI SOVRASCRIVE)
    

if __name__=="__main__":
    main()