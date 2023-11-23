# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:46:17 2023

@author: nicol
"""

URI_LENGTH = 39
URI_PORTION = 17
MAX_IDS_PER_REQUEST = 100  # Maximum number of IDs per Spotify feature request

def spotify_uri_to_id(uri):
    return uri[URI_PORTION:URI_LENGTH]