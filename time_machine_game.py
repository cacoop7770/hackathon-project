import pygame as pg

from gui import Game


class Player:
    """Any of the players (past, present, and future)."""

    def __init__(self, player_num):
        self._player_num
        self._pos = pg.math.Vector2(300, 300)


class CurrentPlayer(Player):
    """Curent player"""

    def __init__(self, player_num):
        Player.__init__(self, player_num)
        self._vy = 0


class PastPlayer(Player):
    """Player in the past"""
    def __init__(self, player_num):
        Player.__init__(self, player_num)
    

class TimeMachine(Game):
    gravity = 0.025
    max_speed = 1
    jump_power = 3

    def __init__(self, controller):
        Game.__init__(self, controller)
        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((650, 600))# Screen is 650x600
        self.vel = [0, 0]
        self.pos = [300, 300]
        self.jump_pos = self.pos
        self.jump = False
        
        
    def handle_event(self, event):
        '''
        Handles the event given

        :param: event: the event given from update_ui
        :type: event: pygame.Event object

        :return: None
        :rtype: None
        '''
         # handle keyboard and ds4
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                #self.pos[0] -= 10
                self.vel[0] = -TimeMachine.max_speed
            if event.key == pg.K_RIGHT:
                self.vel[0] = TimeMachine.max_speed

            if event.key == pg.K_SPACE:
                #print "Jumped!"
                if not self.jump:
                    self.jump_pos = [self.pos[0], self.pos[1]]
                    self.vel[1] = -TimeMachine.jump_power
                    self.jump = True
                
        if event.type == pg.KEYUP:
            self.vel[0] = 0

        if event.type == pg.JOYBUTTONDOWN:
            print "Event type:", event.button
            if event.button == 1:
                #print "Jumped!"
                if not self.jump:
                    self.jump_pos = [self.pos[0], self.pos[1]]
                    self.vel[1] = -TimeMachine.jump_power
                    self.jump = True

        if self.controller:
            #print self.controller.get_numhats()
            hat = self.controller.get_hat(0)
            if hat == (-1, 0):
                # move left
                self.vel[0] = -TimeMachine.max_speed
                print "moving left"
            elif hat == (1, 0):
                #move right
                self.vel[0] = TimeMachine.max_speed
                print "moving right"
            elif hat == (0, 0):
                self.vel[0] = 0
            val = self.controller.get_axis(1)
            if val != 0:
                self.vel[0] = -val * TimeMachine.max_speed
                    
    def gravitation(self):
        if self.jump:
            #print "Using gravity"
            self.vel[1] += TimeMachine.gravity
        
            #print "position:", self.pos, "jumped position:", self.jump_pos
            # unless it lands back on the surface
            if self.pos[1] > self.jump_pos[1]:
                #print "Landed"
                self.jump = False
                self.vel[1] = 0
                #print "position:", self.pos, "jumped position:", self.jump_pos
                self.pos[1] = self.jump_pos[1]
            
    def move(self):
        if self.vel != [0, 0]:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            #print "moving"

    
    def check_win(self):
        ''' 
        Check if the player is close to the goal.
        Display the "winner!" dialog if game is won
        '''
        pass

    def update_ui(self, events):
        '''
        Updates the surface and returns the surface

        :param: events: the events captured from pygame
        :type: events: list

        :return: The surface for this game
        :rtype: pygame.Surface object
        '''
        if self.is_active():
            for event in events:
                self.handle_event(event)

        # update position from speed
        self.move()
        
        # update position from gravity
        self.gravitation()

        ## draw on the surface ##

        # first fill the background
        self.surf.fill((255, 255, 255))

        # then draw the objects
        black = (0, 0, 0)
        pg.draw.rect(self.surf, black, [self.pos[0], self.pos[1], TimeMachine.block_width, TimeMachine.block_height])

        # return the surface so it can be blit
        return self.surf
