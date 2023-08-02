import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyScript:

    def __init__(self):
        self.scope = 'playlist-modify-public'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.track_list = []

    def get_track_id(self, track_name: str, artist: str):
        """
        Takes a track name and the artist name as input to perform a search on spotify to find the track id.
        :param track_name: (str) the title of the song
        :param artist: (str) the artist name
        :return: (str) the spotify track id
        """
        info = self.sp.search(q=f'track: {track_name} artist: {artist}', type='track')
        print(f'Successfully found {track_name} - {artist}')
        track_id = info['tracks']['items'][0]['uri']
        return track_id

    def create_playlist(self, playlist_name: str, user_id: str):
        """
        Creates an empty spotify playlist with a given name on the profile for the user.
        :param playlist_name: (str) the name to give the playlist
        :param user_id: (str) the user id needed to create a playlist on a spotify profile
        :return: (str) the playlist id of the newly created playlist
        """
        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False
        )
        print(f'Successfully created {playlist_name}')
        playlist_id = playlist['id']
        return playlist_id

    def add_tracks_to_playlist(self, playlist_id: str, tracks: list):
        """
        Adds a list of tracks to a given playlist.
        :param playlist_id: (str) the playlist to add tracks to
        :param tracks: (list) a list of track ids
        """
        self.sp.playlist_add_items(
            playlist_id=playlist_id,
            items=tracks
        )
        print('Tracks successfully added to the playlist')

    def get_new_recommendations(self, tracks: list, n_recom: int):
        """
        Creates a list of recommended tracks from a list of seed tracks, based on the spotify recommendations algorithm.
        :param tracks: (list) a list of track ids
        :param n_recom: (int) the number of recommended tracks to get
        :return: the list of recommended tracks
        """
        recommendations = self.sp.recommendations(
            seed_tracks=tracks,
            limit=n_recom
        )
        print(f'Successfully created {n_recom} recommendations')
        return recommendations

    def create_recommended_playlist(self, recom_tracks: list, user_id: str, playlist_name: str):
        """
        Given a list of recommended tracks creates a new playlist, populating it with the recommendations for a given
        user and with the given playlist name
        :param recom_tracks: the list of recommended tracks to add to the playlist
        :param user_id: (str) the user id to create the playlist to the user's profile
        :param playlist_name: (str) the playlist name for the recommendations' playlist
        :return: (str) the playlist id of the playlist
        """
        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False
        )
        print(f'Successfully created {playlist_name}')
        playlist_id = playlist['id']
        self.sp.playlist_add_items(
            playlist_id=playlist_id,
            items=recom_tracks
        )
        print('Recommended tracks successfully added to the playlist')
        return playlist_id

    def get_playlist_items(self, playlist_id: str):
        """
        Given an existing playlist the function return the list of tracks in it.
        :param playlist_id: (str) the id of the playlist
        :return: a list of tracks ids
        """
        track_list = self.sp.playlist_items(playlist_id=playlist_id)
        return track_list
