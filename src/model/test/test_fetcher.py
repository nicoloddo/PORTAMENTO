# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:48:30 2023

@author: nicol
"""

from api.spotify_data_fetcher import SpotifyDataFetcher
import pickle

import test_utils

tests_path = test_utils.TESTS_PATH
TEST_NAME = 'mosiselecta'

folder_path = f'{tests_path}/results/{TEST_NAME}'
test_utils.make_test_results_folder(folder_path)

# define the save callback for the SpotifyDataFetcher
def local_pickle_save(songs, filename):
    save_path = f'{tests_path}/results/{TEST_NAME}/{filename}'
    with open(save_path, "wb+") as f:
            pickle.dump(songs, f)
    
playlists_path = f'{tests_path}/{TEST_NAME}.txt'
fetcher = SpotifyDataFetcher(local_pickle_save)
fetcher.fetch_from_playlists(playlists_path)