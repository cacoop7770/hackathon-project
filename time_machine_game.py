import pygame as pg
from gui import Game


class TimeMachine(Game):
    block_height = 10
    block_width = 10
    def __init__(self, surface):
        Game.__init__(self, surface)
        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((650, 600))# Screen is 650x600
        

    def handle_event(self, event):
         # handle keyboard or ds4
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.pos[0] -= 10
            if event.key == pg.K_RIGHT:
                self.pos[0] += 10
            if event.key == pg.K_UP:
                self.pos[1] -= 10
            if event.key == pg.K_DOWN:
                self.pos[1] += 10

        if event.type == pg.JOYBUTTONDOWN:
            print "Event type:", event.button
            # map the buttons to up, down, left, right
        elif event.type == pg.JOYAXISMOTION:
            if event.axis != 0 and event.value != 0:
                print "Event type:", event.axis, event.value
                # map the joystick to a direction

    def update_ui(self, events):
        if self.is_active():
            for event in events:
                self.handle_event(event)

        ## draw on the surface ##

        # first fill the background
        self.surf.fill((255, 255, 255))

        # then draw the objects
        black = (0, 0, 0)
        pg.draw.rect(self.surf, black, [self.pos[0], self.pos[1], TimeMachine.block_width, TimeMachine.block_height])

        # return the surface so it can be blit
        return self.surf
