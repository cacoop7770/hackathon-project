"""Allow for two games to be run at the same time."""

import json

import pygame as pg
import time
import const
from data_center_game import DataCenter
from delayed_joystick import DelayedJoystick, FutureEvent
from time_machine_game import TimeMachine

# constants
DEBUG = False

# initialize pygame and the display
pg.init()
gameDisplay = pg.display.set_mode((
    const.DC_W + const.MAIN_GAME_W, 
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
with open('levels.json') as f_obj:
    data = json.load(f_obj)
print data

# init the games
tm = TimeMachine(controller)
dc = DataCenter(controller)
delayed_joystick = DelayedJoystick()

# keep track of game time
game_time = time.time()

# keep track of current time delay
game_delay = 0

# start the game
while True:
    val = controller.get_axis(0)
    
    game_time = time.time()

    #if val != 0:
    #    print val
    #    print "\t", controller.get_hat(0)

    # Grab pygame events
    events = pg.event.get()

    # if there is a delay, add all events to the delayed controller
    if game_delay > 0:
        for event in events:
            if event.type == pg.JOYAXISMOTION or event.type == pg.ACTIVEEVENT or event.type == pg.MOUSEMOTION:
                continue
            event_time = game_time + game_delay
            print "Delayed event:\n\tevent: {}\n\tevent time: {}\n\tcurrent time: {}".format(event, event_time, game_time)
            future_event = FutureEvent(event_time, event)
            delayed_joystick.add_event(future_event)
        events = []

    # Check future events and add them to the events
    queued_events = delayed_joystick.queue_event(game_time)
    events.extend(queued_events)
    delayed_joystick.delete_queued_events()
            

    # update the the surface of each game
    #tm_surf_info = tm.update_ui(events)
    #tm_surf = tm_surf_info.get_surface()
    tm_surf = tm.update_ui(events)

    # Only do this if not in debug mode
    if not DEBUG:
        #tm_rect = tm_surf_info.get_rect()
        dc_surf = dc.update_ui(events)

        # Draw each surface onto the main surface
        gameDisplay.blit(dc_surf, (0, 0))

    # Draw each surface onto the main surface
    #gameDisplay.blit(tm_surf, (const.DC_W, 0), tm_rect)
    gameDisplay.blit(tm_surf, (const.DC_W, 0))
    pg.display.flip()

    pg.time.delay(10)# smooth out the animation by adding a delay of 1/10th of a second

