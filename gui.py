import pygame as pg

from ps4 import DeadController


class Game:
    def __init__(self, controller):
        self._running = True
        self.controller = controller # A game uses this (could be a DeadController).
        self._physical_controller = controller # The actual PS4 controller
        self._dead_controller = DeadController() # A controller that does not work.
        self.game_over = False# For game over checks

    def is_active(self):
        return self._running

    def activate(self):
        self._running = True
        self.controller = self._physical_controller

    def deactivate(self):
        self._running = False
        self.controller = self._dead_controller

    def redraw(self):
        """Redraw the surface and return it."""
        raise NotImplementedError

    def handle_event(self, event):
        """Handle the pygame.event."""
        raise NotImplementedError

    def update_world(self):
        """Read controller status (e.g. is a button down) and update the world."""
        raise NotImplementedError

    def update_ui(self, events):
        """Redraw the surface and return it.

        events is a list of pygame.events.
        """
        if self.is_active():
            for event in events:
                self.handle_event(event)
        self.update_world()
        if not self.game_over:
            return self.redraw()
        else:
            return None

