from animation import Animation
from sprite import Sprite


class Entity(Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # Direction of the entity: 0 is left, 1 is right
        self._direction = 0
        self._dead = False
        self._vx = 0
        self._vy = 0
        self._speed = 0

        self.animation = Animation()

    def hit(self):
        # entity dies if hit by default
        self._dead = True

    def _check_horizontal_collisions(self, tiles: list):
        pass

    def _check_vertical_collisions(self, tiles):
        pass

    @property
    def dead(self):
        return self._dead

    @dead.setter
    def dead(self, dead):
        if type(dead) == bool:
            self._dead = dead
