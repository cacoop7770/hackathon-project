import pygame as pg


class Game:
    def __init__(self, controller):
        self._running = True
        self.controller = controller

    def is_active(self):
        return self._running

    def activate(self):
        self._running = True

    def deactivate(self):
        self._running = False

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
        return self.redraw()

