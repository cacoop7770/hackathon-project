import pygame as pg

import const
from gui import Game

white = (255,255,255)
black = (0,0,0)
blue = (0, 0, 255)
clock = pg.time.Clock()

class DataCenter(Game):
    def __init__(self, controller):
        Game.__init__(self, controller)

        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((const.DC_W, const.SCREEN_H))# Screen is 350x600
        self.delay = 0

        ### EDIT CODE1 BELOW ###

        self.gameExit = False

        self.lead_x = 10
        self.lead_y = 10
        self.lead_x_change = 0
        self.lead_y_change = 0


        ### EDIT CODE1 ABOVE ###


    def handle_event(self, event):
        """handle keyboard or ds4"""
        ### EDIT CODE3 BELOW ###
        if event.type == pg.QUIT:
            pg.quit()

        # using the keyboard
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.lead_x_change = -2
            elif event.key == pg.K_RIGHT:
                self.lead_x_change = 2
            elif event.key == pg.K_UP:
                self.lead_y_change = -2
            elif event.key == pg.K_DOWN:
                self.lead_y_change = 2
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                self.lead_x_change = 0
            elif event.key == pg.K_RIGHT:
                self.lead_x_change = 0
            elif event.key == pg.K_UP:
                self.lead_y_change = 0
            elif event.key == pg.K_DOWN:
                self.lead_y_change = 0

        # using the controller
        if self.controller:
            direction_down = self.controller.get_hat(0)
            if direction_down == const.PS_LEFT:
                if self.lead_x >= 0:
                    self.lead_x_change = -2
                else:
                    self.lead_x_change = 0
            elif direction_down == const.PS_RIGHT:
                if self.lead_x < 350:
                    self.lead_x_change = 2
                else:
                    self.lead_x_change = 0
            elif direction_down == const.PS_UP:
                self.lead_y_change = -2
            elif direction_down == const.PS_DOWN:
                self.lead_y_change = 2
            elif direction_down == const.PS_NO_DPAD:
                self.lead_y_change = 0
                self.lead_x_change = 0

        ### EDIT CODE3 ABOVE ###

    def update_world():
        pass

    def get_delay(self):
        return self.delay

    def update_ui(self, events):
        if self.is_active():
            for event in events:
                self.handle_event(event)
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change
        clock.tick(30)

        # return the surface so it can be blit
        return self.redraw()

    def redraw(self):
        """Redraw the datacenter surface and return it."""

        ### EDIT CODE2 BELOW ###
        self.surf.fill(blue)
        pg.draw.rect(self.surf, black, [self.lead_x, self.lead_y, 10, 10])
        ### EDIT CODE2 ABOVE ###

        return self.surf
