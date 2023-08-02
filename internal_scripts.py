import random
from pprint import pprint
from spotify_s import SpotifyScript
from tkinter.simpledialog import askstring
from tkinter import messagebox

spoti_script = SpotifyScript()


def song_data(song: str, artist: str, ids_list: list):
    song_id = spoti_script.get_track_id(track_name=song, artist=artist)
    ids_list.append(song_id)
    if len(ids_list) > 5:
        messagebox.showinfo('Warning', 'Watch out! Only 5 seeds are allowed for creating a list of recommended tracks.'
                                       'If more tracks are passed through, a sample of 5 tracks will be used instead.')


def create_new_playlist(user: str, playlist_name: str, track_list: list):
    playlist_id = spoti_script.create_playlist(playlist_name, user)
    answer = messagebox.askyesno(title='Adding saved songs', message='Do you wish to add the saved songs '
                                                                     'to the playlist?')
    if answer:
        spoti_script.add_tracks_to_playlist(playlist_id, track_list)


def add_to_playlist(playlist_id: str, tracks: list):
    spoti_script.add_tracks_to_playlist(playlist_id, tracks)


def get_recommendations(tracks: list):
    try:
        sample = random.sample(tracks, 5)
    except ValueError:
        sample = tracks
    rec = spoti_script.get_new_recommendations(sample, 20)
    pprint(rec)
    to_playlist = []
    for track in rec['tracks']:
        to_playlist.append(track['id'])
    user = askstring('User ID', "What's your user ID?")
    playlist_name = askstring('Playlist name', "Choose the recommended playlist's name")
    create_new_playlist(user=user, playlist_name=playlist_name, track_list=to_playlist)


def get_playlist_tracks(playlist_id):
    playlist = spoti_script.get_playlist_items(playlist_id=playlist_id)
    playlist_tracks = []
    for i in playlist['items']:
        i_track_id = i['track']['id']
        playlist_tracks.append(i_track_id)
    return playlist_tracks


def get_playlist_tracks_to_list(playlist_id, ids_list: list):
    playlist = spoti_script.get_playlist_items(playlist_id=playlist_id)
    for i in playlist['items']:
        i_track_id = i['track']['id']
        ids_list.append(i_track_id)
