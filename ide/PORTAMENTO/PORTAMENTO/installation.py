# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:32:16 2020

@author: nicol
"""
import paths_info as install

def main():
    
    base_path = r'D:\PROJECTS\PORTAMENTO\users\nic'
    paths = install.Path(base_path)    # COSTRUISCO I PATH BASE
    paths.initialize_default_files(base_path)    # INIZIALIZZO I TABLES (QUESTO LI SOVRASCRIVE)
    

if __name__=="__main__":
    main()