#CITATION: code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# and some functions from https://pythonprogramming.net/adding-sounds-music-pygame/
import pygame

class Music():
    def __init__(self, path):
        self.path = path
        self.loops = -1
        pygame.mixer.music.load(path)

    def start(self):
        pygame.mixer.music.play(loops = -1)
    
    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())