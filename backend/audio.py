import pygame
from pygame import mixer


class Audio:

    def __init__(self, path, is_background_music, play_right_away=True, volume=1):
        self.is_background_music = is_background_music

        if is_background_music:
            mixer.music.load(path)
            mixer.music.set_volume(volume)
        else:
            self.sound = mixer.Sound(path)
            self.sound.set_volume(volume)

        if play_right_away:
            self.play()

    def changeVolume(self, volume):
        if self.is_background_music:
            mixer.music.set_volume(volume)
        else:
            self.sound.set_volume(volume)

    def play(self):
        if self.is_background_music:
            mixer.music.play(-1)
        else:
            self.sound.play()
