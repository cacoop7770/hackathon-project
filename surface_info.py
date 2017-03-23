"""
Information about a surface returned from a game

"""
class SurfaceInformation:
    def __init__(self, surface, rectangle):
        '''
        :param: surface: the surface to be displayed
        :type: surface: pygame.Surface object
        :param: rectangle: where on the surface to focus
        :type: recangle: pygame.Rect
        '''
        self.surf = surface
        self.rect = rectangle

    def get_surface(self):
        return self.surf

    def get_rect(self):
        return self.rect
