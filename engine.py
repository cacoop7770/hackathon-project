import pygame as pg
from time_machine_game import TimeMachine
from data_center_game import DataCenter

pg.init()

gameDisplay = pg.display.set_mode((1000, 600))
pg.display.set_caption("Hackathon project")
pg.display.update()

pg.joystick.init()
try:
    controller = pg.joystick.Joystick(0)
    controller.init()
except pg.error:
    print "No DS4 connected"
    controller = None

# init the games
tm = TimeMachine()
tm.set_controller(controller)
dc = DataCenter()

# start the game
while True:
    val = controller.get_axis(1)
    
    if val != 0:
        print val
        print "\t", controller.get_hat(0)
    # Game goes on right here?
    events = pg.event.get()

    # update the f each
    tm_surf = tm.update_ui(events)
    dc_surf = dc.update_ui(events)

    gameDisplay.blit(dc_surf, (0, 0))
    gameDisplay.blit(tm_surf, (350, 0))
    pg.display.flip()
    pg.time.delay(10)# smooth out the animation by adding a delay of 1/10th of a second
    
    
