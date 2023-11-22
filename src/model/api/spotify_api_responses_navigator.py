# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:18:15 2023

@author: nicol

This module handles the navigation of the structure of Spotify's API responses.
"""

def playlist_items_tracks(playlist):
    return playlist['items']

def playlist_total_tracks(playlist):
    return playlist['tracks']['total']

def track_id(track):
    return track['id']

def track_info(track):
    return track['track']

def track_info_id(track_info):
    return track_info['id']