import os
from tkinter import filedialog
import pygame as pygame
from mutagen.mp3 import MP3


def set_song_title(label, song_title):

    label.setText(song_title)
    label.repaint()



class PlayerFunctions:

    song_list = []
    pygame.init()
    pygame.mixer.init()

    def play_music(self, label):

        if len(self.song_list) > 0:
            for item in self.song_list:
                song_title = os.path.basename(item)
                set_song_title(label, song_title)
                pygame.mixer_music.load(item)
                audio = MP3(item)
                pygame.mixer_music.play()
                pygame.time.wait(int(audio.info.length*1000))




    def next_song(self, label):
        pass

    def previous_song(self, label):
        pass

    def pause(self):
        pass

    def show_music_list(self):
        pass

    def stop_music(self, label):
        pass

    def open_files(self):

        filetypes =(("*.MP3 fájlok",".mp3"),
                    ("*.FLAC fájlok", ".flac"),
                    ("*.MP4 fájlok",".mp4"),
                    ("*.M4A fájlok",".m4a"))

        file_path = filedialog.askopenfilename(filetypes=filetypes)
        self.song_list.append(file_path)


    def open_full_folder(self):
        pass
