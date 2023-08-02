import tkinter
from tkinter import *
from tkinter import messagebox
from internal_scripts import song_data, create_new_playlist, add_to_playlist, get_recommendations, \
    get_playlist_tracks, get_playlist_tracks_to_list
import random

BACKGROUND = '#343434'
LIGHT_BACKGROUND = '#383838'
BOH = '#055E68'
INFO = '#06BAB2'
BUTTONS = '#62A388'
TITLES = '#1DB954'
LABELS = '#B9D2D2'
TITLES_FONT = ('Gotham-Bold', 28)
LABELS_FONT = ('Gotham-Medium', 14)
BUTTONS_FONT = ('Gotham-Medium', 14)
BUTTONS_SMALL_FONT = ('Gotham-Medium', 12)

ids_list = []


class GuiApp(tkinter.Tk):
    """
    The Tkinter app, in which the user can switch between the multiple frames
    """

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        # creating the container
        container = tkinter.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # creating the frames array
        self.frames = {}
        for F in (Index, SaveSongs, Recommendations, Playlists):
            frame = F(container, self)
            self.frames[F] = frame
            frame.configure(background=BACKGROUND)
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Index)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Index(tkinter.Frame):
    """
    The first frame the user sees opening the program, gives instructions on how it works and has links to the
    other more meaningful frames
    Asks the user to input their spotify user id
    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        # frames navigation buttons and frame label
        label = Label(self, text='Index', font=TITLES_FONT, foreground=TITLES, background=BACKGROUND,
                      justify=CENTER)
        label.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        button1 = Button(self, text='Choose Songs', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(SaveSongs))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button1_label = Label(self, text='Input the songs to\nadd them to a playlist\nor to get new songs\n'
                                         'recommendations.', font=LABELS_FONT, foreground=LABELS,
                              background=BACKGROUND)
        button1_label.grid(row=2, column=1, padx=10, pady=10)
        button2 = Button(self, text='Recommendations', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Recommendations))
        button2.grid(row=1, column=2, padx=10, pady=10)
        button2_label = Label(self, text='Get song recommendations\nfrom songs already inputted\nor from '
                                         'existing playlists.', font=LABELS_FONT, foreground=LABELS,
                              background=BACKGROUND)
        button2_label.grid(row=2, column=2, padx=10, pady=10)
        button3 = Button(self, text='Playlist', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Playlists))
        button3.grid(row=1, column=3, padx=10, pady=10)
        button3_label = Label(self, text='Create new playlists\nand add tracks from\ninputted songs or from\n'
                                         'other playlists.', font=LABELS_FONT, foreground=LABELS,
                              background=BACKGROUND)
        button3_label.grid(row=2, column=3, padx=10, pady=10)


class SaveSongs(tkinter.Frame):
    """
    In this frame tracks' names and artists can be added to a python list as part of a dictionary
    The list of dictionaries can be converted into a list of spotify track ids for later usage in the
    playlist creation frame
    Links to other frames are provided through buttons
    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        # frames navigation button and frame label
        label = Label(self, text='Choose Songs', font=TITLES_FONT, foreground=TITLES, background=BACKGROUND,
                      justify=CENTER)
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        button1 = Button(self, text='Index', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Index))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = Button(self, text='Recommendations', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Recommendations))
        button2.grid(row=1, column=2, padx=10, pady=10)
        button3 = Button(self, text='Create a Playlist', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Playlists))
        button3.grid(row=1, column=3, padx=10, pady=10)

        # label and entry for song name
        label_song = Label(self, text="Input the song's name: ", font=LABELS_FONT, foreground=LABELS,
                           background=BACKGROUND)
        label_song.grid(row=2, column=1, padx=10, pady=10)
        song_name = StringVar()
        entry1 = Entry(self, textvariable=song_name, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry1.insert(0, 'Song-Name')
        entry1.focus_force()
        entry1.grid(row=3, column=1, padx=10, pady=10)

        # label and entry for artist name
        label_song = Label(self, text="Input the artist's name: ", font=LABELS_FONT, foreground=LABELS,
                           background=BACKGROUND)
        label_song.grid(row=2, column=2, padx=10, pady=10)
        artist_name = StringVar()
        entry2 = Entry(self, textvariable=artist_name, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry2.insert(0, 'Artist Name')
        entry2.focus_force()
        entry2.grid(row=3, column=2, padx=10, pady=10)

        # defining the save button function
        def save_song_data():
            song_data(song=song_name.get(), artist=artist_name.get(), ids_list=ids_list)
            entry1.delete(0, END)
            entry2.delete(0, END)
            entry1.insert(0, 'Song-Name')
            entry2.insert(0, 'Artist Name')

        # add button
        add_button = Button(self, text='Save track', highlightthickness=0, background=BACKGROUND,
                            foreground=TITLES, font=BUTTONS_SMALL_FONT, activebackground=TITLES, activeforeground=BOH,
                            command=save_song_data)
        add_button.grid(row=4, column=1, padx=10, pady=10)

        # label and entry for playlist-id
        label_playlist = Label(self, text="Input the playlist's Id:", font=LABELS_FONT, foreground=LABELS,
                               background=BACKGROUND)
        label_playlist.grid(row=2, column=3, padx=10, pady=10)
        playlist_id = StringVar()
        entry3 = Entry(self, textvariable=playlist_id, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry3.insert(0, 'Playlist-Id')
        entry3.focus_force()
        entry3.grid(row=3, column=3, padx=10, pady=10)

        # defining save tracks from existing playlist
        def save_playlist_tracks():
            get_playlist_tracks_to_list(playlist_id=playlist_id, ids_list=ids_list)

        # creating button to save playlist tracks
        save_pl_button = Button(self, text='Save playlist', highlightthickness=0, background=BACKGROUND,
                                foreground=TITLES, font=BUTTONS_SMALL_FONT, activebackground=TITLES,
                                activeforeground=BOH, command=save_playlist_tracks)
        save_pl_button.grid(row=4, column=3, padx=10, pady=10)

        # defining show_info function
        def show_info():
            messagebox.showinfo(title='Info', message="In this page you can input songs' names and artists to "
                                                      "search them on Spotify and once the ids are found "
                                                      "songs can be added to playlist through the Playlists frame or "
                                                      "used as seeds to get new song recommendations in the "
                                                      "Recommendations Frame.\nAlternatively a playlist ID can be "
                                                      "inputted to save all songs in it.")

        # adding and info button
        info_button = Button(self, text='Info', highlightthickness=0, background=BACKGROUND, foreground=INFO,
                             font=BUTTONS_SMALL_FONT, activebackground=TITLES, activeforeground=BOH, command=show_info)
        info_button.grid(row=5, column=1, columnspan=3, padx=10, pady=10)


class Recommendations(tkinter.Frame):
    """
    In this frame given a list of 5 seeds from saved tracks or from a playlist a list of 20 recommended tracks are
    provided as output and can be added to a newly created playlist. Necessary data for creating the new playlist is
    asked with messageboxes.
    Links to other frames are provided through buttons.
    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        # frames navigation buttons and frame label
        label = Label(self, text='Discover New Music', font=TITLES_FONT, foreground=TITLES,
                      background=BACKGROUND, justify=CENTER)
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        button1 = Button(self, text='Index', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Index))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = Button(self, text='Choose Songs', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(SaveSongs))
        button2.grid(row=1, column=2, padx=10, pady=10)
        button3 = Button(self, text='Playlists', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Playlists))
        button3.grid(row=1, column=3, padx=10, pady=10)

        # get recommendations from saved songs
        rec_s_label = Label(self, text='Get recommendations \nfrom saved songs.', font=LABELS_FONT, foreground=LABELS,
                            background=BACKGROUND)
        rec_s_label.grid(row=2, column=1, padx=10, pady=10)

        # defining get recommendations from saved function
        def rec_from_saved():
            get_recommendations(tracks=ids_list)

        # creating the recommendations from saved songs button
        rec_s_button = Button(self, text='Get from saved songs', highlightthickness=0, background=BACKGROUND,
                              foreground=TITLES, font=BUTTONS_SMALL_FONT, activebackground=TITLES, activeforeground=BOH,
                              command=rec_from_saved)
        rec_s_button.grid(row=4, column=1, padx=10, pady=10)

        # get recommendations from existing playlist
        rec_p_label = Label(self, text='Get recommendations \nfrom a playlist.', font=LABELS_FONT, foreground=LABELS,
                            background=BACKGROUND)
        rec_p_label.grid(row=2, column=2, padx=10, pady=10)
        playlist_id = StringVar()
        entry1 = Entry(self, textvariable=playlist_id, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry1.insert(0, 'Playlist-Id')
        entry1.grid(row=3, column=2, padx=10, pady=10)

        # defining get recommendations from existing playlist
        def rec_from_playlist():
            playlist_tracks = get_playlist_tracks(playlist_id=playlist_id.get())
            playlist_sample = random.sample(playlist_tracks, 5)
            get_recommendations(tracks=playlist_sample)

        # creating the recommendations from playlist button
        rec_p_button = Button(self, text='Get from playlist', highlightthickness=0, background=BACKGROUND,
                              foreground=TITLES, font=BUTTONS_SMALL_FONT, activebackground=TITLES, activeforeground=BOH,
                              command=rec_from_playlist)
        rec_p_button.grid(row=4, column=2, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=6)

        # defining show_info function
        def show_info():
            messagebox.showinfo(title='Info', message="In this page saved tracks can be use as seed to get new song "
                                                      "recommendations through the Spotify algorithm.\nAlternatively "
                                                      "a playlist ID can be  inputted to use the playlist's tracks "
                                                      "as seed.\nBeware only 5 seeds can be use at each time, therefor "
                                                      "if more are provided a random sample of 5 will be selected.")

        # adding and info button
        info_button = Button(self, text='Info', highlightthickness=0, background=BACKGROUND, foreground=INFO,
                             font=BUTTONS_SMALL_FONT, activebackground=TITLES, activeforeground=BOH, command=show_info)
        info_button.grid(row=5, column=1, columnspan=3, padx=10, pady=10)


class Playlists(tkinter.Frame):
    """
    In this frame the user can create a new playlist and if it does so she/he's asked whether she/he wants
    to add saved songs to the newly created playlist
    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        # frame navigation buttons and frame label
        label = Label(self, text='Manage Playlists', font=TITLES_FONT, foreground=TITLES, background=BACKGROUND,
                      justify=CENTER)
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        button1 = Button(self, text='Index', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Index))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = Button(self, text='Choose Songs', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(SaveSongs))
        button2.grid(row=1, column=2, padx=10, pady=10)
        button3 = Button(self, text='Recommendations', highlightthickness=0, background=BACKGROUND, foreground=TITLES,
                         font=BUTTONS_FONT, activebackground=TITLES, activeforeground=BOH,
                         command=lambda: controller.show_frame(Recommendations))
        button3.grid(row=1, column=3, padx=10, pady=10)

        # playlist name label and button
        playlist_name_label = Label(self, text='Choose a name for\n the playlist:', font=LABELS_FONT, foreground=LABELS,
                                    background=BACKGROUND)
        playlist_name_label.grid(row=2, column=1, padx=10, pady=10)
        playlist_name = StringVar()
        entry1 = Entry(self, textvariable=playlist_name, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry1.insert(0, 'Playlist-Name')
        entry1.focus_force()
        entry1.grid(row=3, column=1, padx=10, pady=10)

        # user id label and entry
        user_id_label = Label(self, text='Enter your user id:', font=LABELS_FONT, foreground=LABELS,
                              background=BACKGROUND)
        user_id_label.grid(row=2, column=2, padx=10, pady=10)
        user_id = StringVar()
        entry2 = Entry(self, textvariable=user_id, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry2.insert(0, 'User-Id')
        entry2.grid(row=3, column=2, padx=10, pady=10)

        # defining create playlist button function
        def create_playlists():
            create_new_playlist(user_id.get(), playlist_name.get(), ids_list)
            entry1.delete(0, END)
            entry2.delete(0, END)
            entry1.insert(0, 'Playlist-Name')
            entry2.insert(0, 'User-Id')

        # create playlist button
        playlist_button = Button(self, text='Create Playlist', highlightthickness=0, background=BACKGROUND,
                                 foreground=TITLES, font=BUTTONS_SMALL_FONT, activebackground=TITLES,
                                 activeforeground=BOH, command=create_playlists)
        playlist_button.grid(row=4, column=1)

        # defining add tracks to playlist button function
        def add_tracks():
            add_to_playlist(playlist_id.get(), ids_list)
            entry3.delete(0, END)
            entry3.insert(0, 'Playlist-Id')

        # add saved songs to existing playlist
        add_songs_label = Label(self, text='Add tracks to an\n existing playlist:', font=LABELS_FONT, foreground=LABELS,
                                background=BACKGROUND)
        add_songs_label.grid(row=2, column=3, padx=10, pady=10)
        playlist_id = StringVar()
        entry3 = Entry(self, textvariable=playlist_id, foreground=BACKGROUND, font=BUTTONS_SMALL_FONT, justify=CENTER)
        entry3.insert(0, 'Playlist-Id')
        entry3.grid(row=3, column=3, padx=10, pady=10)
        add_songs_button = Button(self, text='Add tracks', highlightthickness=0, background=BACKGROUND,
                                  foreground=TITLES, font=BUTTONS_SMALL_FONT, activebackground=TITLES,
                                  activeforeground=BOH, command=add_tracks)
        add_songs_button.grid(row=4, column=3, padx=10, pady=10)

        # defining show_info function
        def show_info():
            messagebox.showinfo(title='Info', message="In this frame playlist can be created and populated with "
                                                      "saved tracks from the 'Add Tracks' frame.\nSaved tracks can"
                                                      " also be added to an existing playlist given the playlist's "
                                                      "ID.")

        # adding and info button
        info_button = Button(self, text='Info', highlightthickness=0, background=BACKGROUND, foreground=INFO,
                             font=BUTTONS_SMALL_FONT, activebackground=TITLES, activeforeground=BOH, command=show_info)
        info_button.grid(row=5, column=1, columnspan=3, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
