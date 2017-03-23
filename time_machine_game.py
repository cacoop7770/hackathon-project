import pygame as pg

import const
from gui import Game
from surface_info import SurfaceInformation

class Player:
    """Any of the players (past, present, and future)."""
    max_speed = 1
    jump_power = 3
    def __init__(self, player_num):
        self._player_num = player_num
        self._pos = pg.math.Vector2(300, 300)

    def get_player_num(self):
        return self._player_num

    def get_position(self):
        return self._pos

    def set_position(self, position_vector):
        self._pos = position_vector


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

    def __init__(self, controller):
        Game.__init__(self, controller)
        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((const.MAIN_GAME_W, const.SCREEN_H))# Screen is 650x600
        self.map_surf = pg.Surface((const.MAP_W, const.MAP_H))
        self.vel = [0, 0]
        self.pos = [300, 300]
        self.jump_pos = self.pos
        self.jump = False

        # keep track of all players
        self.players = []

        # add the first player
        self.add_player()
        
    def add_player(self):
        # first move current player into a past player
        if len(self.players) > 0:
            player_num = self.players[-1].get_player_num()
            pos = self.players[-1].get_position()
            past_player = PastPlayer(player_num)
            past_player.set_position(pos)
            self.players[-1] = past_player

        # now add a new player
        new_player = CurrentPlayer(len(self.players)+1)
        self.players.append(new_player)

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
                self.vel[0] = -Player.max_speed
            if event.key == pg.K_RIGHT:
                self.vel[0] = Player.max_speed

            if event.key == pg.K_SPACE:
                #print "Jumped!"
                if not self.jump:
                    self.jump_pos = [self.pos[0], self.pos[1]]
                    self.vel[1] = -Player.jump_power
                    self.jump = True
                
        if event.type == pg.KEYUP:
            self.vel[0] = 0

        if event.type == pg.JOYBUTTONDOWN:
            print "Event type:", event.button
            if event.button == 1:
                #print "Jumped!"
                if not self.jump:
                    self.jump_pos = [self.pos[0], self.pos[1]]
                    self.vel[1] = -Player.jump_power
                    self.jump = True
            elif event.button == 2:
                # add a new player
                self.add_player()

        if self.controller:
            #print self.controller.get_numhats()
            hat = self.controller.get_hat(0)
            if hat == (-1, 0):
                # move left
                self.vel[0] = -Player.max_speed
                print "moving left"
            elif hat == (1, 0):
                #move right
                self.vel[0] = Player.max_speed
                print "moving right"
            elif hat == (0, 0):
                self.vel[0] = 0
            
            val = self.controller.get_axis(0)
            if val != 0:
                #self.vel[0] = -val * Player.max_speed
                #print val
                pass
                    
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
            
            self.players[-1].set_position(pg.math.Vector2(self.pos[0], self.pos[1]))

    
    def check_win(self):
        ''' 
        Check if the player is close to the goal.
        Display the "winner!" dialog if game is won
        '''
        pass
    
    '''
    def update_ui(self, events):
        Updates the surface and returns the surface

        :param: events: the events captured from pygame
        :type: events: list

        :return: The surface for this game
        :rtype: pygame.Surface object
        # -- handle events --
        if self.is_active():
            for event in events:
                self.handle_event(event)
    '''

    def redraw(self):
        # -- update the game objects--

        # update position from speed
        self.move()

        # update position from gravity
        self.gravitation()

        # use a camera to follow the player
        player_cam = pg.Rect(self.pos[0] - 200, self.pos[1] - 200, self.pos[0] + 200, self.pos[1] + 200)

        # --draw on the surface--

        # first fill the background
        self.surf.fill((255, 255, 255))

        # then draw the objects
        black = (0, 0, 0)
        green = (0, 255, 0)
        #pg.draw.rect(self.surf, black, [self.pos[0], self.pos[1], Player.const.PLAYER_W, Player.const.PLAYER_H])
        player_pos = self.players[-1].get_position()
        pg.draw.rect(self.surf, black, [player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H])# character
        pg.draw.rect(self.surf, green, [400, 300, 20, 20])# reference box

        # draw all of the past players
        font = pg.font.SysFont("monospace", 15)
        for player_num in range(len(self.players)-1):
            player_pos = self.players[player_num].get_position()
            pg.draw.rect(self.surf, black, [player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H])
            label = font.render("Player {}".format(player_num + 1), 1, (255, 0, 0))
            self.surf.blit(label, (player_pos.x, player_pos.y - 10))
            

        # return the surface so it can be blit
        return SurfaceInformation(self.surf, player_cam)
