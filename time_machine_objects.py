'''
Objects for the time machine game

'''
import math
import const

class Platform:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def distance(self, p1, p2):
        """
        Get the distance between two points
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def is_on_platform(self, position):
        '''
        Verify if the given position is on the platform

        :param: position: the position to test
        :type: position: tuple (x, y)

        :return: True if on platform else false
        :rtype: bool
        '''
        # figure out if the position is on a line between start and end points
        epsilon = 0.5
        value = self.distance(position, self.start_pos)\
            + self.distance(position, self.end_pos)\
            - self.distance(self.start_pos, self.end_pos)
        return -epsilon < value < epsilon

    def is_above_platform(self, position):
        '''
        Verify the given position is above the platform
        '''
        # easy way
        return self.start_pos[0] <= position[0] <= self.end_pos[0]\
            and position[1] < self.start_pos[1]\
            and position[1] < self.end_pos[1]

    def is_player_above(self, pos):
        correct_x1 = pos[0] + const.PLAYER_W >= self.start_pos[0]
        correct_x2 = pos[0] <= self.end_pos[0]
        correct_x = correct_x1 and correct_x2

        correct_y1 = pos[1] + const.PLAYER_H < self.start_pos[1]+20
        correct_y2 = pos[1] + const.PLAYER_H < self.end_pos[1]+20
        correct_y = correct_y1 and correct_y2

        return correct_x and correct_y

    def get_height(self, x_pos):
        '''
        Get the platform height at the given x position

        :param: x_pos: x position to get height
        :type: x_pos float

        :return: the height of the platform
        :rtype: float
        '''
        # for now just use start position
        return self.start_pos[1]

    def start(self):
        return self.start_pos

    def end(self):
        return self.end_pos
