import pygame as pg
import math

import const
from gui import Game
from game_states import GameState

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

        self.goal_x = const.DC_W - 100
        self.goal_y = 50

        self.drift_to = [40, const.SCREEN_H - 100]
        self.drifting = False
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
            if direction_down != const.PS_NO_DPAD:
                self.drifting = False
            if direction_down == const.PS_LEFT:
                self.lead_x_change = -2
            elif direction_down == const.PS_RIGHT:
                self.lead_x_change = 2
            elif direction_down == const.PS_UP:
                if self.lead_y > 0:
                    self.lead_y_change = -2
                else:
                    self.lead_y_change = 0
            elif direction_down == const.PS_DOWN:
                self.lead_y_change = 2
            elif direction_down == const.PS_NO_DPAD:
                self.drifting = True
                #self.lead_y_change = 0
                #self.lead_x_change = 0

        ### EDIT CODE3 ABOVE ###

    def update_world(self):
        if not self.is_active():
            self.drifting = True

        if self.lead_x >= 0 and self.lead_x <= const.DC_W:
            self.lead_x += self.lead_x_change
        if self.lead_y >=0 and self.lead_y <= const.SCREEN_H:
            self.lead_y += self.lead_y_change

        if self.lead_x < 0:
            self.lead_x = 0
        if self.lead_x > const.DC_W:
            self.lead_x = const.DC_W
        if self.lead_y < 0:
            self.lead_y = 0
        if self.lead_y > const.SCREEN_H:
            self.lead_y = const.SCREEN_H
        clock.tick(60)

        # move character if not moving
        if self.drifting:
            x_diff = self.drift_to[0] - self.lead_x
            y_diff = self.drift_to[1] - self.lead_y

            # find angle to drift to
            angle = math.atan2(x_diff, y_diff)
            x_component = math.sin(angle)
            y_component = math.cos(angle)

            self.lead_x_change = x_component/2.0
            self.lead_y_change = y_component/2.0

        # losing conditions
        if self.drift_to[0] - 1 < self.lead_x < self.drift_to[0] + 1 \
           and self.drift_to[1] - 1 < self.lead_y < self.drift_to[1] + 1:
            self.state = GameState.GAME_LOSE

    def get_delay(self):
        return self.delay

    def redraw(self):
        """Redraw the datacenter surface and return it."""

        ### EDIT CODE2 BELOW ###
        self.surf.fill((255, 0, 0))

        # draw concentric circles
        pg.draw.circle(self.surf, (255, 125, 0), [self.goal_x, self.goal_y], 700)
        pg.draw.circle(self.surf, (255, 190, 0), [self.goal_x, self.goal_y], 500)
        pg.draw.circle(self.surf, (255, 255, 100), [self.goal_x, self.goal_y], 300)
        #pg.draw.circle(self.surf, (0, 255, 0), [self.goal_x, self.goal_y], 60)
        pg.draw.circle(self.surf, (255, 255, 255), [self.goal_x, self.goal_y], 60)

        pg.draw.rect(self.surf, black, [self.lead_x, self.lead_y, 30, 30])

        # draw the goal
        #pg.draw.rect(self.surf, (0, 255, 0), [self.goal_x, self.goal_y, 50, 50])
        
        # draw signal loss area
        pg.draw.rect(self.surf, (0, 0, 0), [self.drift_to[0], self.drift_to[1], 10, 10])
        font = pg.font.SysFont("monospace", 15)
        label = font.render("signal loss area", 1, (255, 255, 255))
        self.surf.blit(label, (self.drift_to[0], self.drift_to[1] + 30))


        ### EDIT CODE2 ABOVE ###

        return self.surf
