import pygame as pg


class Game:
    def __init__(self):
        self._running = True
        self.controller = None

    def set_controller(self, cont):
        self.controller = cont

    def is_active(self):
        return self._running

    def activate(self):
        self._running = True

    def deactivate(self):
        self._running = False

    def handle_event(self, event):
        pass

    def update_ui(self, events):
        # handle events
        if self.is_active():
            for event in events:
                self.handle_event(event)


