"""Module for the PS4 controller"""

import pygame


class DeadController(pygame.joystick.Joystick):
    """A PS4 controller where no button is being pressed."""

    def get_button(self, button_num):
        """Return that it is not down."""
        return False

    def get_axis(self, axis_num):
        """Return what happens when it is unpressed."""
        return 0


def get_stick_pos(controller, stick):
    """Return an (x, y) pair for the position of the stick.

    controller is a pygame.joystick.Joystick.
    stick is either const.PS_L3 or const.PS_R3.
    """
    pass
