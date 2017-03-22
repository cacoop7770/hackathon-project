import pygame as pg


class Game:
    def __init__(self, main_surface):
        self._running = True
        self.size = self.width, self.height = 800, 600
        self.main_surf = main_surface

        self.surf = pg.Surface((1000, 600))

        self.surf1 = pg.Surface((350, 600))
        self.surf2 = pg.Surface((650, 600))
        #self.rect1 = pg.Rect(0, 0, 400, 600)
        #self.rect2 = pg.Rect(400, 0, 400, 600)

        #self.ball = pg.image.load("ball_image.gif")
        #self.ballrect = self.ball.get_rect()
        self.pos = [300, 300]
        self.speed = [2, 2]
        #self.ball_speed = [2, 2]

    def on_init(self):
        pg.init()
        self._running = True

    def is_active(self):
        return self._running

    def activate(self):
        self._running = True

    def deactivate(self):
        self._running = False

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.deactivate()
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

    def move_rect(self):
        #self.pos[0] += self.speed[0]
        #self.pos[1] += self.speed[1]

        if self.pos[0] > self.width or self.pos[0] < 0:
            self.speed[0] = -self.speed[0]
        if self.pos[1] > self.height or self.pos[1] < 0:
            self.speed[1] = -self.speed[1]

    def update_ui(self, events):
        # handle events
        if self.is_active():
            for event in events:
                self.handle_event(event)

        self.move_rect()

        # update the ui
        self.main_surf.fill((255, 255, 255))
        self.surf.fill((255, 0, 0))

        #self.main_surf.blit(self.surf, (0, 0), self.rect1)
        #self.main_surf.blit(self.surf, (400, 0), self.rect2)

        self.surf1.fill((0, 255, 0))
        self.surf2.fill((255, 255, 255))
        #self.surf2.fill((0, 0, 255))

        pg.draw.rect(self.surf2, (0, 0, 0), [self.pos[0], self.pos[1], 100, 100])
        self.main_surf.blit(self.surf1, (0, 0))
        self.main_surf.blit(self.surf2, (350, 0))
    
        pg.display.flip()

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
