import pygame

pygame.init()

pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print "Event type:", event.button
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis != 0 and event.value != 0:
                print "Event type:", event.axis, event.value
