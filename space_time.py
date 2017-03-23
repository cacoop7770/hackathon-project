class SpaceTime:
    def __init__(self, position, time):
        '''
        An object which hold information for the time
        that a player was at a position

        :param: position: where the player was
        :type: position: pygame.math.Vector2
        :param: time: the time when the player was there
        :type: time: float
        '''
        self._pos = position
        self._time = time

    def get_position(self):
        return self._pos

    def get_time(self):
        return self._time
