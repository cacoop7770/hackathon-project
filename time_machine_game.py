'''
######################################
# TO DO:
# - Seperate redraw code according to current game state
#    -  Some wil share functions such as draw game
# - Add riding a past character
# - Add getting squished by past character
######################################
'''
import pygame as pg

import const
from game_states import GameState
from gui import Game
from surface_info import SurfaceInformation
from space_time import SpaceTime
from players import Player, CurrentPlayer, PastPlayer
from time_machine_objects import Platform

class TimeMachine(Game):
    def __init__(self, controller, levels_config=None):
        Game.__init__(self, controller)
        # The main surface is in self.main_surf
        # so want to blit my own surface there
        self.disp_surf = pg.Surface((const.MAIN_GAME_W, const.SCREEN_H))# Screen is 650x600
        self.map_surf = pg.Surface((const.MAP_W, const.MAP_H))
        self.vel = [0, 0]
        #self.start_pos = [300, 300]
        #self.pos = [300, 300]
        self.jump = False
        self.levels_config = levels_config
        self.current_level = 1
        self.pos = self.get_level_start(self.current_level)
        print "Starting at", self.pos

        # keep track of time/# of updates
        self.time = 0
        self.new_time = 0
        self.past_time = 0# the moment of time you changed the time

        # keep track of all players
        self.players = []

        # add the first player
        self.add_player()

        self._backwards = False

        # don't let the player move in some situations
        self.allow_move = True
        self.player_to_ride = -1

        # keep track of platforms
        self.platforms = self.get_platforms(1)
        self.current_landing_y = 1000

    def get_platforms(self, level_num):
        if not self.levels_config:
            return []
        level_text = "Level {}".format(level_num)
        if level_text not in self.levels_config:
            print "Level {} not in the configs".format(level_num)
        this_level = self.levels_config[level_text]

        # draw lines
        platforms = []
        lines = [this_level[key] for key in this_level if key.startswith("line")]
        for line in lines:
            start_pos = (line[0], line[1])
            end_pos = (line[2], line[3])
            platform = Platform(start_pos, end_pos)
            platforms.append(platform)
        return platforms

    def add_player(self, end_time=None):
        # first move current player into a past player
        if len(self.players) > 0:
            player_num = self.players[-1].get_player_num()
            pos = self.players[-1].get_position()
            positions = self.players[-1].get_positions()

            past_player = PastPlayer(player_num, self.time, pos, end_time)
            print "Added a player at time: {} with finish time: {}".format(self.time, end_time)
            past_player.set_position(pos)
            past_player.set_positions(positions)

            self.players[-1] = past_player

        # now add a new player
        start = self.get_level_start(self.current_level)
        new_player_pos = pg.math.Vector2(start[0], start[1])
        new_player = CurrentPlayer(len(self.players)+1, self.new_time, start_pos=new_player_pos)
        #new_player.set_position(pg.math.Vector2(const.PORTAL_X, const.PORTAL_Y))
        self.pos = new_player.get_position()
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
        elif self.state == GameState.POPUP:
            self.handle_popup_event(event)

    def handle_popup_event(self, event):
        '''
        Handles the event for the game when there is a popup

        :param: event: the event given from update_ui
        :type: event: pygame.Event object

        :return: None
        :rtype: None
        '''
        if event.type == pg.JOYBUTTONDOWN:
            if event.button == const.PS_X:
                self.state = GameState.PLAY
                self.restart()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.state = GameState.PLAY
                self.restart()

    def handle_backwards_event(self, event):
        '''
        Handles the event for the game when moving backwards in time

        :param: event: the event given from update_ui
        :type: event: pygame.Event object

        :return: None
        :rtype: None
        '''

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.state = GameState.PLAY
                self.past_time = self.time
                self.time = self.new_time

                # add a new player when going back in time
                self.add_player(self.past_time)

                return
            if event.key == pg.K_LEFT:
                self.new_time -= 2
            if event.key == pg.K_RIGHT:
                self.new_time += 2

        if event.type == pg.JOYBUTTONDOWN:
            if event.button == const.PS_TRI:
                # pressing triangle stops the time machine
                #self._backwards = False
                self.state = GameState.PLAY
                self.past_time = self.time
                self.time = self.new_time

                # add a new player when going back in time
                self.add_player(self.past_time)

                return

        if self.controller:
            hat = self.controller.get_hat(0)
            if hat == const.PS_LEFT:
                # move lefti
                self.new_time -= 2
            elif hat == const.PS_RIGHT:
                # move right
                self.new_time += 2

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
                self.vel[0] = -const.max_speed
            if event.key == pg.K_RIGHT:
                self.vel[0] = const.max_speed

            if event.key == pg.K_SPACE:
                #print "Jumped!"
                if not self.jump:
                    self.vel[1] = -const.jump_power
                    self.jump = True
            if event.key == pg.K_BACKSPACE:
                self.state = GameState.TIME_TRAVEL
                return

        if event.type == pg.KEYUP:
            self.vel[0] = 0

        if event.type == pg.JOYBUTTONDOWN:
            print "Event type:", event.button
            if event.button == const.PS_X:
                #print "Jumped!"
                if not self.jump:
                    self.vel[1] = -const.jump_power
                    self.jump = True
            elif event.button == const.PS_O:
                # add a new player
                self.add_player()
            elif event.button == const.PS_TRI:
                # pressing triangle starts the time machine
                self.state = GameState.TIME_TRAVEL
                return

        if self.controller:
            #print self.controller.get_numhats()
            hat = self.controller.get_hat(0)
            if hat == const.PS_LEFT:
                # move left
                self.vel[0] = -const.max_speed
            elif hat == const.PS_RIGHT:
                #move right
                self.vel[0] = const.max_speed
            elif hat == const.PS_NO_DPAD:
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
            if self.time % 1 == 0:
                player_pos = self.players[-1].get_position()
                self.players[-1].record_position(player_pos, self.time)

        # move past players
        if self.time < self.past_time:
            self.move_past_players_through_time()

        # update position from speed
        self.move()

        # update position from gravity
        self.gravitation()

        # do not let player run into other players
        if self.check_player_collisions():
            return

        # Check if player won
        if self.check_win():
            self.current_level += 1
            self.state = GameState.POPUP
            #self.draw_popup("Congrats! You beat level {}. Press X to continue".format(self.current_level - 1), (100,100))
            print "Moving onto level {}".format(self.current_level)
            self.allow_move = False

    def gravitation(self):
        '''
        Handles gravity and moves the character accordingly
        '''

        # unless it lands back on the surface
        # change this so it can jump on top of another player

         # check platforms for landing on
        landings_to_check = []
        for platform in self.platforms:
            if platform.is_player_above(self.pos):
                landings_to_check.append(platform.get_height(self.pos))

        # if that platform isn't under you anymore
        if self.current_landing_y not in landings_to_check:
            self.current_landing_y = 1000

         #landing_y = 1000#self.start_pos[1]
        # then check the players to land on
        self.player_to_ride = -1
        for i in range(len(self.players)-1):
            player_pos = self.players[i].get_position()
            if player_pos == None:
                continue
            player_x = player_pos.x
            player_y = player_pos.y
            if self.pos[0] > player_x - const.PLAYER_W and self.pos[0] < player_x + const.PLAYER_W:
                if self.pos[1] < player_y:
                    self.current_landing_y = player_y #- const.PLAYER_H
                    self.player_to_ride = i

        for landing in landings_to_check:
            if landing < self.current_landing_y:
                #if self.pos[1] + const.PLAYER_H < landing:
                self.current_landing_y = landing

        # perform the gravity
        if self.jump or self.pos[1] + const.PLAYER_H < self.current_landing_y:
            self.vel[1] += const.gravity

        # stopping conditions
        if self.pos[1] + const.PLAYER_H > self.current_landing_y:
            # make sure on way down
            if self.vel[1] > 0:
                self.jump = False
                self.vel[1] = 0

        # Check if player died
        if self.pos[1] > const.DEATH_Y:
            self.state = GameState.GAME_LOSE

    def check_player_collisions(self):
        '''
        Returns true if there is a collision
        '''
        my_rect = pg.Rect(self.pos[0], self.pos[1], const.PLAYER_W, const.PLAYER_H)
        for player in self.players:
            if not isinstance(player, PastPlayer):
                continue
            if not player.exists(self.time) or player.expired(self.time):
                continue
            player_pos = player.get_position()
            player_rect = pg.Rect(player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H)
            '''
            if self.pos[0] + const.PLAYER_W > player_pos.x and self.pos[0] < player_pos.x + const.PLAYER_W:
                if player_pos.y <= self.pos[1] <= player_pos.y + const.PLAYER_H \
                  or self.pos[1] <= player_pos.y <= self.pos[1] + const.PLAYER_H:
            '''
            if my_rect.colliderect(player_rect):
                    self.vel = [0, 0]
                    print "player pos:", self.pos, "other pos", player_pos
                    # move off player
                    # if on the left then move a bit to the left
                    if self.player_to_ride == -1:
                        if self.pos[0] < player_pos.x:
                            self.pos[0] = player_pos.x - const.PLAYER_W
                        else:
                            #self.pos[0] += 1
                            self.pos[0] = player_pos.x + const.PLAYER_W
                        return True
        return False

    def move(self):
        if not self.allow_move:
            return

        # if riding ontop a player
        if self.player_to_ride != -1 and not self.jump:
            ride = self.players[self.player_to_ride]
            self.pos[0] = ride.get_position().x
            self.pos[1] = ride.get_position().y - const.PLAYER_H

        #if self.vel != [0, 0]:
        # do not let player run into other players
        #if self.check_player_collisions():
        #    return
        '''
        my_rect = pg.Rect(self.pos[0], self.pos[1], const.PLAYER_W, const.PLAYER_H)
        for player in self.players:
            if not isinstance(player, PastPlayer):
                continue
            if not player.exists(self.time) or player.expired(self.time):
                continue
            player_pos = player.get_position()
            player_rect = pg.Rect(player_pos.x, player_pos.y, const.PLAYER_W, const.PLAYER_H)
            if my_rect.colliderect(player_rect):
                    self.vel = [0, 0]
                    print "player pos:", self.pos, "other pos", player_pos
                    # move off player
                    # if on the left then move a bit to the left
                    if self.player_to_ride == -1:
                        if self.pos[0] < player_pos.x:
                            self.pos[0] = player_pos.x - const.PLAYER_W
                        else:
                            #self.pos[0] += 1
                            self.pos[0] = player_pos.x + const.PLAYER_W
                        return
        '''


        # allow the player to move if not touching another player
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.players[-1].set_position(pg.math.Vector2(self.pos[0], self.pos[1]))

    def check_win(self):
        '''
        Check if the player is close to the goal.
        Display the "winner!" dialog if game is won
        '''
        if not self.levels_config:
            return False
        level_text = "Level {}".format(self.current_level)
        if level_text not in self.levels_config:
            print "Level {} not in the configs".format(self.current_level)
        this_level = self.levels_config[level_text]

        end_pos = this_level["end"]
        if end_pos[0] -40 < self.pos[0] < end_pos[0] + 40:
            if end_pos[1] - 40 < self.pos[1] < end_pos[1] + 40:
                return True
        return False

    def draw_popup(self, text, disp_location, popup_size=None):
        '''
        Draws a popup with given text on the screen

        :param: text: the text to display
        :type: text: str
        :param: disp_location: Location on the display surface for the popup
        :type: disp_location: tuple (x, y)

        '''
        # draw a new surface
        size = width, height =(400, 100) if not popup_size else popup_size
        popup = pg.Surface(size)
        popup.fill((0, 0, 0))
        popup.fill((255, 255, 255), [10, 10, width - 20, height - 20])

        # write the text on the surface
        font = pg.font.SysFont("monospace", 15)
        label = font.render(text, 1, (0, 0, 0))
        popup.blit(label, (20, 20))

        self.disp_surf.blit(popup, disp_location)


    def draw_text(self, text, pos, color=(0, 0, 0), disp=False):
        """
        Draws text onto the map surface

        :param: text: The text to be drawn
        :type: text: str
        :param: pos: Position of the text on the map
        :type: pos: position array (ie (x, y))
        :param: color: the color of the text
        :type: color: color arrray (r,g,b)
        :param: disp: for display surface or map?
        :type: disp: bool
        """
        font = pg.font.SysFont("monospace", 15)
        label = font.render(text, 1, color)
        if not disp:
            self.map_surf.blit(label, pos)
        else:
            self.disp_surf.blit(label, pos)

    def draw_portal(self, pos):
        """Draw the portal at this position.

        pos represents the top left corner of where the player
        will spawn.
        """
        p_h = const.PLAYER_H
        p_h2 = p_h / 2
        p_w = const.PLAYER_W
        p_w2 = p_w / 2
        rad = const.PORTAL_R
        diam = const.PORTAL_D
        port_surf = pg.Surface((diam, diam), flags=pg.SRCALPHA)
        pg.draw.circle(port_surf, (255,0,0), (rad, rad), rad)
        rect = pg.Rect(rad - p_w / 2, rad - p_h / 2, p_w, p_h)
        pg.draw.rect(port_surf, (255, 255, 0), rect, const.PLAYER_THICK)
        self.map_surf.blit(port_surf, pos - (pg.math.Vector2(rad, rad) - pg.math.Vector2(p_w2, p_h2)))
#        self.draw_text("Portal", (pos[0], pos[1] - 20), color=(255, 0, 0))

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
        #print "time: {}, new_time: {}, tick_positon: {}".format(self.time, self.new_time, tick_position)
        pg.draw.circle(machine_surface, (255, 0, 0), [int(tick_position), 110], 20)

        # write the time you go back to
        font = pg.font.SysFont("monospace", 15)
        label = font.render("Time: {}".format(self.new_time), 1, (0, 0, 0))
        machine_surface.blit(label, (10, 10))


        self.disp_surf.blit(machine_surface, (0, 450))

    def move_past_players_through_time(self):
        for player in self.players:
            if isinstance(player, PastPlayer):
                # get past position
                if player.exists(self.time):
                    position = player.get_position_at_time(self.time)
                    player.set_position(position)

    def draw_time(self, pos):
        #self.draw_text("Current Time: {}".format(self.time), (10, 10), disp=True)
        font = pg.font.SysFont("monospace", 15)
        label = font.render("Current Time: {}".format(self.time), 1, (0, 0, 0))
        self.map_surf.blit(label, pos)

    def get_level_start(self, level_num):
        if not self.levels_config:
            return
        level_text = "Level {}".format(level_num)
        if level_text not in self.levels_config:
            print "Level {} not in the configs".format(level_num)
        this_level = self.levels_config[level_text]
        return this_level["start"]

    def draw_level(self, level_num):
        if not self.levels_config:
            return
        level_text = "Level {}".format(level_num)
        if level_text not in self.levels_config:
            print "Level {} not in the configs".format(level_num)
        this_level = self.levels_config[level_text]

        # draw lines
        for platform in self.platforms:
            #lines = [this_level[key] for key in this_level if key.startswith("line")]
            #for line in lines:
            start_pos = platform.start()
            end_pos = platform.end()
            pg.draw.line(self.map_surf, (0, 0, 0), start_pos, end_pos, 5)

        # Draw the beginning portal
        self.draw_portal(pos=this_level["start"])

        # Draw the end portal
        self.draw_portal(pos=this_level["end"])

    def map_to_display(self):
        """Draw the map onto the display surface (camera code here)."""
        #todo: Move camera around in time travel mode
        player_pos = self.players[-1].get_position()
        camera_pos = (
            player_pos.x - const.HALF_SCREEN_W,
            player_pos.y - const.HALF_SCREEN_H
        )
        rect = pg.Rect(player_pos.x-const.HALF_SCREEN_W, player_pos.y -const.HALF_SCREEN_H, const.MAIN_GAME_W, const.SCREEN_H)
        self.disp_surf.blit(self.map_surf, (0,0), rect) #todo: fix

    def restart(self):
        start = self.get_level_start(self.current_level)
        self.pos = [start[0], start[1]]
        self.platforms = self.get_platforms(self.current_level)
        self.allow_move = True
        self.vel = [0, 0]
        self.players = []
        self.add_player()

    def draw_player(self, pos, player_num):
        """Draw a player.

        All players look alike except for their number written in the center.
        pos can be a Vector2 or tuple.
        """
        font = pg.font.SysFont('monospace', 50)
        gray = (128, 128, 128)
        black = (0, 0, 0)
        rect = pg.Rect(pos, (const.PLAYER_W, const.PLAYER_H))
        pg.draw.rect(self.map_surf, gray, rect)
        pg.draw.rect(self.map_surf, black, rect, const.PLAYER_THICK)
        text_surf = font.render(str(player_num), True, black, gray)
        text_pos = pos + pg.math.Vector2(
            (const.PLAYER_W - text_surf.get_width()) / 2,
            (const.PLAYER_H - text_surf.get_height()) / 2
        )
        self.map_surf.blit(text_surf, text_pos)

    def redraw(self):
        # -- update the game objects--
        black = (0, 0, 0)
        green = (0, 255, 0)
        white = (255, 255, 255)
        yellow = (255, 255, 0)
        blue = (0, 0, 255)
        font = pg.font.SysFont("monospace", 15)

        # first fill the backgrounds
        self.map_surf.fill(white)
        self.disp_surf.fill(black)
        pg.draw.rect(self.map_surf, green, [400, 300, 20, 20])# reference box
        #pg.draw.rect(self.map_surf, green, [0, 20, 20, 20])# reference box

        # Draw the beginning portal
        #self.draw_portal()

        # draw the level objects
        self.draw_level(self.current_level)

        # draw the current time in the upper left corner (draw this later)
        #self.draw_time()

        ## TIME TRAVEL
        if self.state == GameState.TIME_TRAVEL:
            # redraw the players at self.new_time
            for player_num in range(len(self.players)):
                player = self.players[player_num]
                player_pos = player.get_position_at_time(self.new_time)
                if player_pos == None:
                    continue
                # do not draw a player if it does not exist
                if not player.exists(self.new_time) or player.expired(self.new_time):
                    continue
                self.draw_player((player_pos.x, player_pos.y), player_num + 1)
            self.map_to_display()
            self.draw_machine_ui()

        else:
            ## NOT TIME TRAVEL
            # then draw the current player
            crnt_player = self.players[-1]
            player_pos = crnt_player.get_position()
            self.draw_player(player_pos, crnt_player.get_player_num())
            self.draw_time((player_pos.x-20, player_pos.y - 20))

            # draw all of the past players
            for player_num in range(len(self.players)-1):
                player = self.players[player_num]
                player_pos = self.players[player_num].get_position()
                if player_pos == None:
                    continue
                if not player.exists(self.time) or player.expired(self.time):
                    continue
                self.draw_player((player_pos.x, player_pos.y), player_num + 1)
            self.map_to_display()

        if self.state == GameState.POPUP:
            self.draw_popup("Congrats! You beat level {}. Press X to continue.".format(self.current_level - 1), (100,100), popup_size=(600, 100))

        # return the surface so it can be blit

        #self.draw_popup("this is text", (100, 100))
        return self.disp_surf
