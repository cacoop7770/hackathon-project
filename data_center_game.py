import pygame as pg
from gui import Game

class DataCenter(Game):
    def __init__(self, controller):
        Game.__init__(self, controller)

        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((DC_W, SCREEN_H))

    def handle_event(self, event):
         # handle keyboard or ds4
         pass

    def redraw(self):
        """Redraw the datacenter surface and return it."""
        self.surf.fill((255, 0, 0))
        return self.surf
