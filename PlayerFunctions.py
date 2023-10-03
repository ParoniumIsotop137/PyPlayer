import os
import sys
import time
from tkinter import filedialog

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl, pyqtSignal, QObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QFileDialog

from ListWindow import Ui_listWindow


class PlayerFunctions:


    listWindow = None
    playlist_window = None
    player = QMediaPlayer()
    playlist = QMediaPlaylist()
    i = 0
    isPlaying = False


    def play_music(self, label):

        self.player.setPlaylist(self.playlist)
        self.player.play()
        self.isPlaying = True
        label.setText(os.path.basename(self.player.currentMedia().canonicalUrl().toString()))
        label.repaint()

    def next_song(self, label):

        if self.isPlaying:
            self.player.stop()
            self.playlist.next()
            self.player.play()
        else:
            self.playlist.next()
            self.player.play()

    def previous_song(self, label):

        if self.isPlaying:
            self.player.stop()
            self.playlist.previous()
            self.player.play()
        else:
            self.playlist.previous()
            self.player.play()

    def pause(self):
        if self.isPlaying:
            self.player.pause()
            self.isPlaying = False
        elif self.player.PausedState:
            self.player.play()
            self.isPlaying = True

    def show_music_list(self):

        if self.listWindow is None:
            self.listWindow = QtWidgets.QListWidget()
            self.playlist_window = Ui_listWindow()
            self.playlist_window.setupUi(self.listWindow)
            self.playlist_window.set_items(self.playlist)
            self.listWindow.show()
        else:
            self.playlist_window.update_items(self.playlist)
            self.listWindow.show()
        



    def stop_music(self, label):
        if self.isPlaying:
            self.player.stop()
            self.isPlaying = False

    def open_files(self):

        filetypes =(("*.MP3 fájlok",".mp3"),
                    ("*.FLAC fájlok", ".flac"),
                    ("*.MP4 fájlok",".mp4"),
                    ("*.M4A fájlok",".m4a"))

        file_path = filedialog.askopenfilename(filetypes=filetypes)
        content = QMediaContent(QUrl.fromLocalFile(file_path))
        self.playlist.addMedia(content)



    def open_full_folder(self):

        filetypes =(("MP3 fájlok", "*.mp3"),
                    ("FLAC fájlok", "*.flac"),
                    ("MP4 fájlok", "*.mp4"),
                    ("M4A fájlok", "*.m4a"))

        file_paths, _ = QFileDialog.getOpenFileNames(None, "Fájlok kiválasztása", "", ";;".join(f"{name} ({pattern})" for name, pattern in filetypes))

        if file_paths:
             for file_path in file_paths:
                media = QMediaContent(QUrl.fromLocalFile(file_path))
                self.playlist.addMedia(media)


    def set_song_title(self, label, song_title):

        label.setText(song_title)
        label.repaint()

    def close_list_window(self):

        self.listWindow.close()

