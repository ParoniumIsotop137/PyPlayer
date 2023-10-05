import os
import sys
import threading
import time
from multiprocessing.sharedctypes import synchronized
from tkinter import filedialog


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import PlayerMainWindow
from ListWindow import Ui_listWindow

def update_label(player, label):

    song_title = os.path.basename(player.currentMedia().canonicalUrl().toString())
    label.setText(song_title)
    label.repaint()

class PlayerFunctions:


    listWindow = None
    playlist_window = None
    player = QMediaPlayer()
    playlist = QMediaPlaylist()
    i = 0
    isPlaying = False
    stopButton = False
    label = None


    def play_music(self, label):

        if not self.playlist.isEmpty():
            try:

                self.label = label
                self.player.setPlaylist(self.playlist)

                self.player.play()
                self.isPlaying = True
                self.stopButton = False
                song_title = os.path.basename(self.player.currentMedia().canonicalUrl().toString())
                label.setText(song_title)
                self.playlist.currentMediaChanged.connect(lambda: update_label(self.player, label))
            except Exception as e:
                message = QMessageBox()
                message.setIcon(QMessageBox.Critical)
                message.setWindowTitle("Hiba történt!")
                message.setText(str(e))
                message.exec()
        else:
            self.missing_files_message()

    def next_song(self, label):
        if not self.playlist.isEmpty():
            if self.isPlaying:
                self.player.stop()
                self.playlist.next()
                self.player.play()
            else:
                self.playlist.next()
                self.player.play()
        else:
            self.missing_files_message()

    def previous_song(self, label):
        if not self.playlist.isEmpty():
            if self.isPlaying:
                self.player.stop()
                self.playlist.previous()
                self.player.play()
            else:
                self.playlist.previous()
                self.player.play()
        else:
            self.missing_files_message()

    def pause(self):
        if not self.playlist.isEmpty():
            if self.isPlaying:
                self.player.pause()
                self.isPlaying = False

            elif self.stopButton:
                 self.player.stop()
                 self.isPlaying = False

            elif self.player.PausedState:
                  self.player.play()
                  self.isPlaying = True
        else:
            self.missing_files_message()

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

        if not self.playlist.isEmpty():
            if self.isPlaying:
                self.player.stop()
                self.isPlaying = False
                self.stopButton = True
        else:
            self.missing_files_message()

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
        else:
            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setWindowTitle("Fájbetöltés sikertelen")
            message.setText("Nem került betöltésre egyetlen fájl sem. Az eddig betöltött zenék megtekinthetőek a zenelistában.")
            message.exec()
    def close_list_window(self):

        self.listWindow.close()


    def missing_files_message(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Warning)
        message.setWindowTitle("Nincs lejátszandó fájl!")
        message.setText("Még nem került betöltésre egy zenefájl sem a menüből!")
        message.exec()



