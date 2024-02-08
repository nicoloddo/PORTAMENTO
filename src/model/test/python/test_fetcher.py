# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:48:30 2023

@author: nicol
"""

import test_utils

from core.spotify_data_fetcher import SpotifyDataFetcher
import pickle

tests_path = test_utils.TESTS_PATH
test_name = test_utils.TEST_NAME

folder_path = f'{tests_path}/results/{test_name}'
test_utils.make_test_results_folder(folder_path)

# define the save callback for the SpotifyDataFetcher
def local_pickle_save(songs, filename):
    save_path = f'{tests_path}/results/{test_name}/{filename}'
    with open(save_path, "wb+") as f:
            pickle.dump(songs, f)
    
playlists_path = f'{tests_path}/test_input/{test_name}.txt'
fetcher = SpotifyDataFetcher(local_pickle_save)
fetcher.fetch_from_playlists(playlists_path)