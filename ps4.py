"""Module for the PS4 controller"""

import const


class DeadController:
    """A PS4 controller where no button is being pressed."""

    def get_button(self, button_num):
        """Return that it is not down."""
        return False

    def get_axis(self, axis_num):
        """Return what happens when it is unpressed."""
        return 0

    def get_hat(self, hat_num):
        """Return an unpressed hat."""
        return (0, 0)


def get_stick_pos(controller, stick):
    """Return an (x, y) pair for the position of the stick.

    controller is a pygame.joystick.Joystick.
    stick is either const.PS_L3 or const.PS_R3.
    """
    if stick == const.PS_L3:
        x_axis = PS_JOYSTICK_LEFT_X
        y_axis = PS_JOYSTICK_LEFT_Y
    elif stick == const.PS_R3:
        x_axis = PS_JOYSTICK_RIGHT_X
        y_axis = PS_JOYSTICK_RIGHT_Y
    else:
        raise Exception('stick needs to be left stick or right stick.')

    return (controller.get_axis(x_axis), controller.get_axis(y_axis))


