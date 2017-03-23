import pygame as pg
from gui import Game

white = (255,255,255)
black = (0,0,0)

class DataCenter(Game):
    def __init__(self, controller):
        Game.__init__(self, controller)

        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((DC_W, SCREEN_H))

        ### EDIT CODE1 BELOW ###

        self.gameExit = False

        self.lead_x = 300
        self.lead_y = 300

        ### EDIT CODE1 ABOVE ###


    def handle_event(self, event):
         """handle keyboard or ds4"""

         ### EDIT CODE3 BELOW ###

        if event.type == pg.QUIT:
            pygame.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.lead_x -= 10
            if event.key == pg.K_RIGHT:
                self.lead_x += 10

        ### EDIT CODE3 ABOVE ###


    def redraw(self):
        """Redraw the datacenter surface and return it."""
        ### EDIT CODE2 BELOW ###
        self.surf.fill(white)
        pg.draw.rect(self.surf, black, [lead_x, lead_y, 10, 10])
        ### EDIT CODE2 ABOVE ###

        return self.surf
