"""Allow for two games to be run at the same time."""

import json
import argparse

import pygame as pg
import time
import const
from data_center_game import DataCenter
from delayed_joystick import DelayedJoystick, FutureEvent
from game_states import GameState
from time_machine_game import TimeMachine

parser = argparse.ArgumentParser()
parser.add_argument('game', nargs='?', choices=['tm', 'dc'], help='Launch this game only')
args = parser.parse_args()

# initialize pygame and the display
pg.init()
if args.game is None:
    display_width = const.DC_W + const.MAIN_GAME_W
elif args.game == 'tm':
    display_width = const.MAIN_GAME_W
else:
    display_width = const.DC_W
gameDisplay = pg.display.set_mode((
    display_width,
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
if args.game is None:
    tm = TimeMachine(controller, levels_config=data)
    dc = DataCenter(controller)
    dc.deactivate()
elif args.game == 'tm':
    tm = TimeMachine(controller, levels_config=data)
else:
    dc = DataCenter(controller)
delayed_joystick = DelayedJoystick()

# keep track of game time
game_time = time.time()

# keep track of current time delay
game_delay = 0

# start the game
while True:
    game_time = time.time()

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

    # change active game
    '''
<<<<<<< HEAD
    for event in events:
        if event.type == pg.JOYBUTTONDOWN:
            if event.button == const.PS_R1:
                tm.activate()
                dc.deactivate()
            elif event.button == const.PS_L1:
                tm.deactivate()
                dc.activate()

    # update the the surface of each game
    tm_surf = tm.update_ui(events)

    # tm_surf is None if game is over
    if not tm_surf:
        print "Game over!"
        break

    # Only do this if not in debug mode
    if not DEBUG:
        #tm_rect = tm_surf_info.get_rect()
=======
    '''
    if args.game is None:
        for event in events:
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == const.PS_R1:
                    tm.activate()
                    dc.deactivate()
                elif event.button == const.PS_L1:
                    tm.deactivate()
                    dc.activate()

    if args.game is None:
        # update the the surface of each game
        tm_surf = tm.update_ui(events)
        dc_surf = dc.update_ui(events)
        if not tm_surf or not dc_surf:
            if tm.state == GameState.GAME_WIN:
                print "YOU WON!"
                break
            print "Game over!"
            break

        gameDisplay.blit(dc_surf, (0, 0))
        gameDisplay.blit(tm_surf, (const.DC_W, 0))
    elif args.game == 'tm':
        tm_surf = tm.update_ui(events)
        gameDisplay.blit(tm_surf, (0, 0))
    else:
        #>>>>>>> c2d3dfa24017c170c2c004ed5e0b491a57af09d0
        dc_surf = dc.update_ui(events)
        gameDisplay.blit(dc_surf, (0, 0))

    pg.display.flip()

#    pg.time.delay(10)# smooth out the animation by adding a delay of 1/10th of a second
