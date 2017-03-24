import pygame as pg
from space_time import SpaceTime

class Player:
    """Any of the players (past, present, and future)."""
    def __init__(self, player_num, time, start_pos, finish_time=None):
        self._player_num = player_num
        self._pos = start_pos#pg.math.Vector2(300, 300)# Arbitrary start position
        self._positions = []# Collection of SpaceTime objects
        self.start_time = time# game time when the player started
        self.finish_time = finish_time# When the player became a Past Player

    def get_player_num(self):
        return self._player_num

    def get_position(self):
        return self._pos

    def expired(self, time):
        '''
        Check if player is expired at given time
        '''
        if not self.finish_time:
            return False
        if time > self.finish_time:
            return True
        return False

    def exists(self, time):
        '''
        Checks if player exists at given time
        '''
        '''
        if self.finish_time:
            if time > self.finish_time:
                print "PLAYER DOES NOT EXIST at time {} b/c finish: {}".format(time, self.finish_time)
                return False
        '''
        return time > self.start_time

    def set_position(self, position_vector):
        self._pos = position_vector

    def record_position(self, position, time):
        '''
        Record where and when the player was

        :param: position: where the player was
        :type: position: pygame.math.Vector2
        :param: time: the time when the player was there
        :type: time: float
        '''
        new_space_time = SpaceTime(position, time)
        self._positions.append(new_space_time)

    def get_position_at_time(self, time):
        '''
        Get where the player was at the given time

        :param: position: where the player was
        :type: position: pygame.math.Vector2
        :param: time: the time when the player was there
        :type: time: float

        :return: player position
        :rtype: pygame.math.Vector2
        '''
        if not self.exists(time):
            return None

        for i in range(len(self._positions)):
            t = self._positions[i].get_time()
            if t > time:
                return self._positions[i-1].get_position()
        return self.get_position()

    def get_positions(self):
        return self._positions

    def set_positions(self, space_times):
        self._positions = space_times


class CurrentPlayer(Player):
    """Curent player"""

    def __init__(self, player_num, time, start_pos=pg.math.Vector2(300, 300)):
        Player.__init__(self, player_num, time, start_pos)
        self._vy = 0



class PastPlayer(Player):
    """Player in the past"""
    def __init__(self, player_num, time, start_pos=pg.math.Vector2(300, 300), finish_time=None):
        Player.__init__(self, player_num, time, start_pos, finish_time)

