# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:35:32 2023

@author: nicol

This file defines the classes to fetch songs from the Spotify API
Example usage:
    
def local_pickle_save(songs, filename):
    save_path = f'./mosiselecta/{filename}'
    with open(save_path, "wb+") as f:
            pickle.dump(songs, f)
        
playlists_path = './mosiselecta.txt'
fetcher = SpotifyDataFetcher(local_pickle_save)
fetcher.fetch_from_playlists(playlists_path)
"""

from common.utils import spotify_uri_to_id, MAX_IDS_PER_REQUEST

import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import api.spotify_api_responses_navigator as api_nav
    
class SpotifyDataFetcher:
    def __init__(self, save_callback = (lambda songs, filename: None), batch_size = MAX_IDS_PER_REQUEST):
        """
        Initialize the SpotifyDataFetcher instance. This class can be used in Desktop deployments, or to test.
        This class uses the SpotifyBatchDataFetcher class, described below, which handles the fetching in batches of playlists.
        The Batch fetcher will be used in Cloud deployment services which have timeout limits, with a handler that directly uses
        that class, like this one does. For this reason, this class can be used for testing purposes since its mechanic
        is equivalent to the one of cloud handlers.        
        
        :param save_callback(): Function used for the saving process. 
        It needs the songs to save and the filename as input.
        The default process does not save anything.
        
        :param batch_size: Number of songs to process in each batch. Default: defined in utils.py
        
        Attributes:
        - self.sp: The Spotify access point, using the Spotipy library.
        """
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
        self.batch_size = batch_size
        self.save_callback = save_callback


    def fetch_from_playlists(self, playlist_file_path):
        """
        Fetch data in batches from Spotify playlists using the SpotifyBatchDataFetcher, merges the batches and saves.
        
        :param playlist_file_path: Path to the file containing Spotify playlist URIs.
        :param check_other_datasets_callback: Function to check if a track was already retrieved in another dataset.
        :return: Pandas DataFrame with Spotify track data.
        """
        playlists = self._read_playlist_file(playlist_file_path)

        for playlist_uri in playlists:
            print(playlist_uri)
            self.fetch_handler(playlist_uri, 0, self.batch_size)
    
    def fetch_handler(self, playlist_uri, start_index, batch_size):
        """
        Basic copy of the lamda handler for AWS
        """
        # Initialize the SpotifyDataFetcher
        playlist_fetcher = SpotifyBatchDataFetcher(self.sp, playlist_uri, batch_size)
        playlist_fetcher.fetch_playlist()
        # Fetch songs from the playlist
        songs = playlist_fetcher.fetch_batch_from_playlist(start_index,  (lambda track_id: False))

        # Save the fetched songs
        filename = f'{spotify_uri_to_id(playlist_uri)}_{start_index}.pickle'
        self.save_callback(songs, filename)

        # Check if there are more songs to fetch and enqueue the next batch
        total_songs = playlist_fetcher.total_songs_in_playlist()  # Implement this method in SpotifyDataFetcher
        if start_index + batch_size < total_songs:
            next_start_index = start_index + batch_size
            next_batch_size = batch_size # You can manipulate this to only use the remaining amount of songs for the last batch
            self.fetch_handler(playlist_uri, next_start_index, next_batch_size)
        
        print({'statusCode': 200, 'body': 'Batch processed'})

    
    def _read_playlist_file(self, playlist_file_path):
        """
        Read the playlist file and return a list of playlist URIs.
        :return: List of playlist URIs.
        """
        with open(playlist_file_path, "r") as file:
            playlists = file.read().splitlines()
        return playlists


class SpotifyBatchDataFetcher:
    def __init__(self, sp, playlist_uri, batch_size):
        """
        Initialize the SpotifyBatchDataFetcher instance. The class has the task of fetching a batch of songs
        from a given playlist.
        
        :param sp: The Spotify access point, using the Spotipy library.
        :param playlist_uri: The uri of the playlist from which to retrieve the batch.
        :param batch_size: Number of songs to process in each batch.

        Attributes:
        - self.sp: The Spotify access point, using the Spotipy library.
        - self.batch_tracks: A list that holds detailed information for each track in the batch.
          This includes track name, artist, album, and features. The list structure allows for 
          ordered storage and easy manipulation of track data.
        - self.playlist_uri: The uri of the playlist from which to retrieve the batch.
        - self.playlist: The playlist from which we are retrieving the batch.
        - self.n_songs_playlist: The number of songs in the playlist from which we are retrieving the batch.
        """
        self.sp = sp
        
        self.batch_tracks = [] # Stores information of each track in case it is used as a batch fetcher
        self.playlist_uri = playlist_uri
        self.playlist = None # The playlist of the given batch
        self.n_songs_playlist = None # The number of songs in the playlist of the given batch
    
    def fetch_playlist(self):
        """
        Fetches information on the playlist of the batch at issue.
        """
        self.playlist = self._get_playlist(self.playlist_uri)
        self.n_songs_playlist = api_nav.playlist_total_tracks(self.playlist)
    
    def fetch_batch_from_playlist(self, start_index, filter_callback):
        """
        Fetch a batch of songs from Spotify playlists uris and return a pandas DataFrame with desired columns.
        
        :param start_index: The index of the song in the playlist from which the batch to retrieve starts.
        :param filter_callback: Function to filter tracks (e.g. check if a track was already retrieved in the current dataset.)
        :return: Pandas DataFrame with Spotify track data.
        """
        playlist_items = self.sp.playlist_items(self.playlist_uri, offset = start_index)
        playlist_tracks = api_nav.playlist_items_tracks(playlist_items)
        processed_playlist_tracks = self._process_playlist_tracks(playlist_tracks, filter_callback)
        final_tracks = self._get_tracks_features(processed_playlist_tracks)
        self.batch_tracks.extend(final_tracks)
        dataset = pd.DataFrame(self.batch_tracks)
        return dataset
    
    def total_songs_in_playlist(self):
        return self.n_songs_playlist

    def _get_playlist(self, playlist_uri):
        """
        Fetch playlist info from given its id.
        :param playlist_id: Spotify playlist ID.
        :return: List of track information dictionaries.
        """
        playlist_id = spotify_uri_to_id(playlist_uri)
        playlist = self.sp.playlist(playlist_id) # Fetch playlist
        return playlist
    
    def _process_playlist_tracks(self, tracks, filter_callback):
        """
        Process tracks from a single playlist. 
        This method filters out tracks based on the filter_callback, adds the features and formats each unique track.
        
        :param tracks: List of track information dictionaries from a single playlist.
        :param filter_callback: Function to filter tracks (e.g. check if a track was already retrieved in the current dataset.)
        :return: A list of processed and formatted tracks.
        
        Note: The track structure is substituted here with its track_info
        """
        processed_tracks = []
        
        for track in tracks:
            track = api_nav.track_info(track)
            track_id = api_nav.track_info_id(track)
            if not filter_callback(track_id):
                formatted_track = self._format_track_info(track)
                processed_tracks.append(formatted_track)
        
        return processed_tracks

    def _get_tracks_features(self, tracks):
        """
        Fetch audio features for a list of tracks from Spotify and format them.
        :param tracks: List of track information dictionaries.
        :return: List of dictionaries with combined track info and formatted features.
        """
        track_ids = [api_nav.track_info_id(track) for track in tracks]
        features = self.sp.audio_features(track_ids)  # Fetch features
        formatted_features = self._format_features(features)

        # Combine track info with formatted features
        combined_tracks_with_features = []
        for track in tracks:
            # Look for the track's features in the formatted_features list.
            # The next() function with a generator expression is used here to find the first
            # occurrence in formatted_features where the 'id' matches the current track's 'id'.
            # If no matching features are found, it returns None.
            track_features = next((item for item in formatted_features if item['id'] == track['id']), None)
        
            # If matching features are found, combine the track info and its features.
            if track_features:
                # The ** operator is used to unpack the track dictionary and the track_features
                # dictionary into a new dictionary, effectively merging them.
                # This combined dictionary contains all the information and features of the track.
                combined = {**track, **track_features}
        
                # Add the combined dictionary to the list of tracks with their features.
                combined_tracks_with_features.append(combined)

        combined_tracks_with_features = self._format_features(combined_tracks_with_features)
        return combined_tracks_with_features

    def _format_features(self, tracks):
        """
        Format the features of the tracks by removing unnecessary fields.
        :param features: List of feature dictionaries for each track.
        :return: List of formatted feature dictionaries.
        """
        irrelevant_fields = ['type', 'analysis_url', 'uri', 'track_href']
        for track in tracks:
            for field in irrelevant_fields:
                if field in track:
                    del track[field]
        return tracks

    def _format_track_info(self, track):
        """
        Format track information to include only relevant data.
        This function cleans up the track dictionary by removing unnecessary fields
        and restructuring some parts for better usability.

        :param track: Dictionary of track information.
        :return: Formatted track information dictionary.
        """

        # Remove irrelevant fields from track details
        irrelevant_fields = [
            'available_markets', 'episode', 'explicit', 'external_ids', 
            'is_local', 'sections_confidences', 'segments_confidences', 'track'
        ]
        
        song_analysis_irrelevant_fields = [ # These irrelevant fields were used in the version that performed song analysis
            'analysis_channels', 'analysis_sample_rate', 'code_version', 'codestring', 'duration',
            'echoprint_version', 'echoprintstring', 'end_of_fade_in', 'num_samples', 'offset_seconds',
            'rhythm_version', 'rhythmstring', 'sample_md5', 'start_of_fade_out', 'synch_version',
            'synchstring', 'window_seconds', 'key', 'loudness', 'mode', 'tempo', 'time_signature',
            'meta', 'bars', 'beats', 'tatums'
        ]
        
        for field in irrelevant_fields:
            if field in track:
                del track[field]

        # Process segments to flatten pitch and timbre data
        for segment in track.get('segments', []):
            self._flatten_segment_data(segment)

        return track

    def _flatten_segment_data(self, segment):
        """
        Flatten pitch and timbre data in a segment for easier analysis.

        :param segment: Segment dictionary with 'pitches' and 'timbre' lists.
        """
        for i, pitch in enumerate(segment.get('pitches', [])):
            segment[f'pitch_{i}'] = pitch
        del segment['pitches']

        for i, timbre in enumerate(segment.get('timbre', [])):
            segment[f'timbre_{i}'] = timbre
        del segment['timbre']

    def _extract_confidences(self, items):
        """
        Extract confidence values from sections or segments.

        :param items: List of dictionaries (sections or segments).
        :return: List of dictionaries with only confidence values.
        """
        confidences = []
        for item in items:
            confidence = {key: value for key, value in item.items() if 'confidence' in key}
            confidences.append(confidence)
        return confidences