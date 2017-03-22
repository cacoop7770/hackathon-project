import pygame as pg
from gui import Game

class DataCenter(Game):
    def __init__(self):
        Game.__init__(self)

        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((350, 600))# Screen is 650x600

    def handle_event(self, event):
         # handle keyboard or ds4
         pass

    def update_ui(self, events):
        if self.is_active():
            for event in events:
                self.handle_event(event)

        # draw on the surface here
        # make sure to draw inside of self.surf
        

        # Choose background color of surface (r,g,b)
        self.surf.fill((0, 255, 0))

        # return the surface so it can be blit
        return self.surf
