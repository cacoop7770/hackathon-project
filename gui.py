import pygame as pg


class Game:
    def __init__(self):
        self._running = True
        self.controller = None

    def set_controller(self, cont):
        self.controller = cont

    def is_active(self):
        return self._running

    def activate(self):
        self._running = True

    def deactivate(self):
        self._running = False

    def handle_event(self, event):
        pass

    def update_ui(self, events):
        # handle events
        if self.is_active():
            for event in events:
                self.handle_event(event)


if __name__ == '__main__':
    # this is where the gui is created and maintained
    pg.init()

    gameDisplay = pg.display.set_mode((1000, 600))
    pg.display.set_caption("Hackathon project")
    pg.display.update()

    pg.joystick.init()
    try:
        controller = pg.joystick.Joystick(0)
        controller.init()
    except:
        print "No DS4 connected"
        controller = None

    game = Game(gameDisplay)


    # Game loop
    while True:
       # pg.display.update()

        events = pg.event.get()

        game.update_ui(events)
        

        # check which is active
        # and then update THAT ui to handle "events"
        
        
        # DC update
        
        # TM update

        pg.display.flip()
