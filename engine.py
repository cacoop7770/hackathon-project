"""Allow for two games to be run at the same time."""

import json

import pygame as pg

from time_machine_game import TimeMachine
from data_center_game import DataCenter
import const

# initialize pygame and the display
pg.init()
gameDisplay = pg.display.set_mode((
    const.DC_W + MAIN_GAME_W, 
    const.SCREEN_H
))
pg.display.set_caption("Hackathon project")
pg.display.update()

# Initialize the joystick
pg.joystick.init()
try:
    controller = pg.joystick.Joystick(0)
    controller.init()
except pg.error:
    print "No DS4 connected"
    controller = None

# grab the game configuration
f = open("levels.json", "r")

data =json.load(f)
f.close()
print data

# init the games
tm = TimeMachine(controller)
dc = DataCenter(controller)

# start the game
while True:
    val = controller.get_axis(1)
    
    if val != 0:
        print val
        print "\t", controller.get_hat(0)

    # Grab pygame events
    events = pg.event.get()

    # update the the surface of each game
    tm_surf = tm.update_ui(events)
    dc_surf = dc.update_ui(events)

    # Draw each surface onto the main surface
    gameDisplay.blit(dc_surf, (0, 0))
    gameDisplay.blit(tm_surf, (350, 0))
    pg.display.flip()
    pg.time.delay(10)# smooth out the animation by adding a delay of 1/10th of a second
    
