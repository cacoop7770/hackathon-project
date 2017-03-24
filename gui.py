import pygame as pg

from game_states import GameState
from ps4 import DeadController


class Game:
    def __init__(self, controller):
        self._running = True
        self.controller = controller # A game uses this (could be a DeadController).
        self._physical_controller = controller # The actual PS4 controller
        self._dead_controller = DeadController() # A controller that does not work.
        self.state = GameState.PLAY 

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

    def __draw_active(self, surf):
        """Draw the active outline on this surface."""
        pg.draw.rect(surf, (255, 0, 0), pg.Rect(0, 0, surf.get_width(), surf.get_height()), 10)

    def update_ui(self, events):
        """Redraw the surface and return it.

        events is a list of pygame.events.
        """
        if self.is_active():
            for event in events:
                self.handle_event(event)
        self.update_world()
        
        rtn = self.redraw()
        if not rtn:
            return None
        if self.is_active():
            self.__draw_active(rtn)

        if self.state not in [GameState.GAME_WIN, GameState.GAME_LOSE]:
            return rtn
        else:
            return None

