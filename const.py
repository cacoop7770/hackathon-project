"""Module for constants"""

# PlayStation buttons
PS_SQUARE = 0
PS_X = 1
PS_O = 2
PS_TRI = 3
PS_L1 = 4
PS_R1 = 5
PS_L2 = 6
PS_R2 = 7
PS_SHARE = 8
PS_OPTIONS = 9
PS_L3 = 10
PS_R3 = 11
PS_PS = 12# PS button
PS_TOUCH = 13

# D-pad
PS_LEFT = (-1, 0)
PS_RIGHT = (1, 0)
PS_UP = (0, 1)
PS_DOWN = (0, -1)
PS_NO_DPAD = (0, 0)

# Joysticks
PS_JOYSTICK_LEFT_X = 0
PS_JOYSTICK_LEFT_Y = 1
PS_JOYSTICK_RIGHT_X = 2
PS_JOYSTICK_RIGHT_Y = 3

# Screen sizes
DC_W = 450
MAIN_GAME_W = 1000# Time machine game
SCREEN_H = 800
#DC_W = 350
#MAIN_GAME_W = 650# Time machine game
#SCREEN_H = 600
HALF_SCREEN_H = SCREEN_H / 2
HALF_SCREEN_W = (DC_W + MAIN_GAME_W) / 2

PLAYER_H = 100
PLAYER_W = 50
PLAYER_THICK = 3

# Here for now
#gravity = 0.025
gravity = 0.3
#max_speed = 1
max_speed = 4
#jump_power = 3
jump_power = 9

MAP_W = 3000
MAP_H = 3000

# position of the portal
PORTAL_X = 300
PORTAL_Y = 300

# Convenience
PORTAL_R = int(.75 * PLAYER_H) # radius
PORTAL_D = 2 * PORTAL_R # diameter

DEATH_Y = 2000
