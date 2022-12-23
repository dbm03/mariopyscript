import pyxel

from settings import ITEM_SIZE, GRAVITY
from sprite import Sprite
import level_tiles

class Item(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, ITEM_SIZE, ITEM_SIZE)
        # level will delete the item if used is True
        self._used = False
        # velocity vectors so the item can move
        self._vx = 0
        self._vy = 0
        # the default max gravity acceleration of items is smaller than the max acceleration of entities,
        # so they look lighter
        self._max_accel = 3

    def update(self, tiles: list):
        self._vy += GRAVITY
        # limit gravity acceleration
        if self._vy > self._max_accel:
            self._vy = self._max_accel

        self.x += self._vx
        self._check_horizontal_collisions(tiles)
        self.y += self._vy
        self._check_vertical_collisions(tiles)

    def _check_horizontal_collisions(self, tiles):
        for tile in tiles:
            if self.intersects(tile):
                if self._vx > 0:
                    self.right = tile.left
                else:
                    self.left = tile.right

    def _check_vertical_collisions(self, tiles):
        for tile in tiles:
            if self.intersects(tile):
                if self._vy > 0:
                    self.bottom = tile.top
                else:
                    self.top = tile.bottom

    def use(self):
        self._used = True

    @property
    def used(self):
        return self._used


class Mushroom(Item):
    def __init__(self, x, y, direction: int):
        super().__init__(x, y)
        # speed of the mushroom
        self._speed = 1
        if type(direction) == int:
            if direction == 0 or direction == 1:
                self._direction = direction
            else:
                raise ValueError("Value of the 'direction' parameter is not valid")
        else:
            raise TypeError("The type of the parameter 'direction' is not valid")

    def update(self, tiles):
        super().update(tiles)

        if self._direction == 0:
            self._vx = -self._speed
        else:
            self._vx = self._speed

    # rewritten so mushroom changes direction when colliding with a tile
    def _check_horizontal_collisions(self, tiles):
        for tile in tiles:
            if self.intersects(tile):
                if self._direction == 0:
                    self.left = tile.right
                    self._direction = 1
                else:
                    self.right = tile.left
                    self._direction = 0

    # rewritten so mushroom can change direction when touched by a bouncing block
    def _check_vertical_collisions(self, tiles):
        for tile in tiles:
            if self.intersects(tile):
                if self._vy > 0:
                    self.bottom = tile.top
                    if isinstance(tile, level_tiles.Block):
                        if tile.broken or tile.bouncing:
                            # make mushroom jump
                            self._vy = -10
                            # change direction of the mushroom
                            if self._direction == 0:
                                self._direction = 1
                            else:
                                self._direction = 0
                else:
                    self.top = tile.bottom

    def draw(self, x_shift):
        pyxel.blt(self.x + x_shift, self.y, 0, 48, 32, 16, 16, 12)
