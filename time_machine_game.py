'''
######################################
# TO DO:
# - Implement the game states
# - Maybe add more states
# - Seperate redraw code according to current game state
#    -  Some wil share functions such as draw game
# - 
######################################
'''
import pygame as pg

import const
from gui import Game
from surface_info import SurfaceInformation
from space_time import SpaceTime
from players import Player, CurrentPlayer, PastPlayer

class GameState:
    PLAY = 0
    TIME_TRAVEL = 1
    GAME_WIN = 2
    GAME_LOSE = 3

class TimeMachine(Game):
    gravity = 0.025

    def __init__(self, controller):
        Game.__init__(self, controller)
        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.surf = pg.Surface((const.MAIN_GAME_W, const.SCREEN_H))# Screen is 650x600
        self.map_surf = pg.Surface((const.MAP_W, const.MAP_H))
        self.vel = [0, 0]
        self.start_pos = [300, 300]
        self.pos = [300, 300]
        self.jump_pos = self.pos
        self.jump = False

        # keep track of time/# of updates
        self.time = 0
        self.new_time = 0
        self.past_time = 0# the moment of time you changed the time

        # keep track of all players
        self.players = []

        # add the first player
        self.add_player()

        self._backwards = False
        self.state = GameState.PLAY

    def add_player(self):
        # first move current player into a past player
        if len(self.players) > 0:
            player_num = self.players[-1].get_player_num()
            pos = self.players[-1].get_position()
            positions = self.players[-1].get_positions()
            past_player = PastPlayer(player_num, self.time)
            past_player.set_position(pos)
            past_player.set_positions(positions)

            self.players[-1] = past_player

        # now add a new player
        new_player = CurrentPlayer(len(self.players)+1, self.time)
        self.players.append(new_player)

    def handle_event(self, event):
        '''
        Handles the event given

        :param: event: the event given from update_ui
        :type: event: pygame.Event object

        :return: None
        :rtype: None
        '''
        if self.state == GameState.PLAY:
            self.handle_game_event(event)
        elif self.state == GameState.TIME_TRAVEL:
            self.handle_backwards_event(event)

    def handle_backwards_event(self, event):
        '''
        Handles the event for the game when moving backwards in time

        :param: event: the event given from update_ui
        :type: event: pygame.Event object

        :return: None
        :rtype: None
        '''
        if event.type == pg.JOYBUTTONDOWN:
            if event.button == const.PS_TRI:
                # pressing triangle stops the time machine
                #self._backwards = False
                self.state = GameState.PLAY
                self.past_time = self.time
                self.time = self.new_time
                
                # add a new player when going back in time
                self.add_player()
                return
        
        if self.controller:
            hat = self.controller.get_hat(0)
            if hat == const.PS_LEFT:
                # move left
                self.new_time -= 2
                print "moving tick left"
            elif hat == const.PS_RIGHT:
                # move right
                self.new_time += 2
                print "moving tick right"
        
        if self.new_time > self.time:
            self.new_time = self.time
        if self.new_time < 0:
            self.new_time = 0
    
    def handle_game_event(self, event):
        '''
        Handles the event for the game

        :param: event: the event given from update_ui
        :type: event: pygame.Event object

        :return: None
        :rtype: None
        '''
        self.new_time = self.time

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
                    #self.jump_pos = [self.pos[0], self.pos[1]]
                    self.vel[1] = -Player.jump_power
                    self.jump = True
                
        if event.type == pg.KEYUP:
            self.vel[0] = 0

        if event.type == pg.JOYBUTTONDOWN:
            print "Event type:", event.button
            if event.button == const.PS_X:
                #print "Jumped!"
                if not self.jump:
                    #self.jump_pos = [self.pos[0], self.pos[1]]
                    self.vel[1] = -Player.jump_power
                    self.jump = True
            elif event.button == const.PS_O:
                # add a new player
                self.add_player()
            elif event.button == const.PS_TRI:
                # pressing triangle starts the time machine
                #self._backwards = True
                self.state = GameState.TIME_TRAVEL
                return

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
            
            val = self.controller.get_axis(const.PS_JOYSTICK_LEFT_X)
            if val != 0:
                #self.vel[0] = -val * Player.max_speed
                #print val
                pass

    def update_world(self):
        '''
        Update the state of the world before redrawing
        '''

        # Move time forward and  store current player's position
        if self.state == GameState.PLAY:
            self.time += 1
            if self.time % 10 == 0:
                player_pos = self.players[-1].get_position()
                self.players[-1].record_position(player_pos, self.time)

        # update position from speed
        self.move()

        # update position from gravity
        self.gravitation()

        # move past players
        if self.time < self.past_time:
            self.move_past_players_through_time()



    def gravitation(self):
        '''
        Handles gravity and moves the character accordingly
        '''
        
        #print "position:", self.pos, "jumped position:", self.jump_pos
        # unless it lands back on the surface
        # change this so it can jump on top of another player
        
        landing_y = self.start_pos[1]
        for i in range(len(self.players)-1):
            player_pos = self.players[i].get_position()
            if player_pos == None:
                continue
            player_x = player_pos.x
            player_y = player_pos.y
            if self.pos[0] > player_x - const.PLAYER_W and self.pos[0] < player_x + const.PLAYER_W:
                landing_y = player_y - const.PLAYER_H
                print landing_y, "Changed to player:", i
                

        if self.jump or self.pos[1] < landing_y:
            #print "Using gravity"
            self.vel[1] += TimeMachine.gravity
            print landing_y

        if self.pos[1] > landing_y:
            #print "Landed"
            self.jump = False
            self.vel[1] = 0
            #print "position:", self.pos, "jumped position:", self.jump_pos
            self.pos[1] = landing_y
            
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

    def draw_machine_ui(self):
        '''
        Draw the strip for the time machine thingy
        '''

        # draw the surface for the time machine
        machine_surface = pg.Surface((650, 150))
        
        # make the strip grey
        machine_surface.fill((100, 100, 100))

        # draw the timeline
        pg.draw.rect(machine_surface, (0, 0, 0), [100, 100, 500, 20])
        pg.draw.rect(machine_surface, (0, 0, 0), [100, 95, 10, 30])# left side
        pg.draw.rect(machine_surface, (0, 0, 0), [600, 95, 10, 30])# right side
        
        # draw the circle which indicates when in time to go
        # how far to move per button press?
        tick_position = 550.0*(float(self.new_time) / float(self.time)) + 50
        print "time: {}, new_time: {}, tick_positon: {}".format(self.time, self.new_time, tick_position)
        pg.draw.circle(machine_surface, (255, 0, 0), [int(tick_position), 110], 20)

        # write the time you go back to
        font = pg.font.SysFont("monospace", 15)
        label = font.render("Time: {}".format(self.new_time), 1, (0, 0, 0))
        machine_surface.blit(label, (10, 10))
         

        self.surf.blit(machine_surface, (0, 450))

    def move_past_players_through_time(self):
        for player in self.players:
            if isinstance(player, PastPlayer):
                # get past position
                if player.exists(self.time):
                    position = player.get_position_at_time(self.time)
                    player.set_position(position)

    def draw_time(self):
        font = pg.font.SysFont("monospace", 15)
        label = font.render("Current Time: {}".format(self.time), 1, (0, 0, 0))
        self.surf.blit(label, (10, 10))

    def redraw(self):
        # -- update the game objects--
        black = (0, 0, 0)
        green = (0, 255, 0)
        font = pg.font.SysFont("monospace", 15)

        # first fill the background
        self.surf.fill((255, 255, 255))
        pg.draw.rect(self.surf, green, [400, 300, 20, 20])# reference box
        
        # draw the current time in the upper left corner
        self.draw_time() 

        if self.state == GameState.TIME_TRAVEL:
            self.draw_machine_ui()
            # redraw the players at self.new_time
            for player_num in range(len(self.players)):
                player_pos = self.players[player_num].get_position_at_time(self.new_time)
                if player_pos == None:
                    continue
                pg.draw.rect(self.surf, black, [player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H])
                label = font.render("Player {}".format(player_num + 1), 1, (255, 0, 0))
                self.surf.blit(label, (player_pos.x, player_pos.y - 10))
            return self.surf

        # then draw the objects
        player_pos = self.players[-1].get_position()
        pg.draw.rect(self.surf, black, [player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H])# character

        # draw all of the past players
        for player_num in range(len(self.players)-1):
            player_pos = self.players[player_num].get_position()
            if player_pos == None:
                continue
            pg.draw.rect(self.surf, black, [player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H])
            label = font.render("Player {}".format(player_num + 1), 1, (255, 0, 0))
            self.surf.blit(label, (player_pos.x, player_pos.y - 10))


        # return the surface so it can be blit
        return self.surf
