from animation import Animation, Image
from items import Item, Mushroom
from sprite import Sprite
import pyxel
from settings import TILE_SIZE, ITEM_SIZE
from settings import FPS


class Tile(Sprite):
    def __init__(self, x, y, width=TILE_SIZE, height=TILE_SIZE):
        super().__init__(x, y, width, height)
        self._broken = False

    def update(self):
        pass

    def destroy(self):
        self._broken = True

    @property
    def broken(self):
        return self._broken


class Block(Tile):
    def __init__(self, x, y, breakable: bool = False):
        super().__init__(x, y)
        '''
        @param breakable: makes the block a breakable block by Mario when affected by the mushroom power up
        '''
        if type(breakable) == bool:
            self._breakable = breakable
        else:
            raise TypeError("The type of the parameters is not valid")

        self._block_image = Image(0, 16, 16, 16, 0)
        # True when small Mario hits the block
        self._bouncing = False
        # the original y coordinate is stored so the block comes back to its original place after bouncing
        # only _bounce_y is changed
        self._bounce_y = self.y
        # counter for the bounce animation
        self._bounce_count = 0
        # will bounce for half a second
        self._bounce_time = FPS/3

    def update(self):
        if self._bouncing:
            # if bounce has finished
            if self._bounce_count >= self._bounce_time:
                # reset variables to default
                self._bounce_y = self.y
                self._bouncing = False
                self._bounce_count = 0
            else:
                # move block up
                self._bounce_y -= 1
                # count time
                self._bounce_count += 1

    @property
    def bouncing(self):
        return self._bouncing

    def draw(self, x_shift: int):
        self._block_image.draw(self.x + x_shift, self._bounce_y)

    def bounce(self):
        self._bouncing = True

    def destroy(self):
        self._broken = True

    @property
    def breakable(self):
        return self._breakable

class StairBlock(Tile):
    def __init__(self,x,y):
        super().__init__(x,y)
        self._stair_image = Image(48,16,16,16,0)

    def draw(self, x_shift):
        self._stair_image.draw(self.x + x_shift, self.y)

class CoinBlock(Tile):
    def __init__(self, x, y, coins: int):
        super().__init__(x, y)
        self.coins = coins
        self._gives_coins = True
        self._block_image = Image(0, 16, 16, 16, 0)
        self._used_block_image = Image(80, 0, 16, 16, 0)

    def hit(self):
        if self.coins > 0:
            self.coins -= 1
        else:
            self._gives_coins = False

    def draw(self, x_shift: int):
        if self.coins > 0:
            self._block_image.draw(self.x + x_shift, self.y)
        else:
            self._used_block_image.draw(self.x + x_shift, self.y)

    @property
    def gives_coins(self):
        return self._gives_coins


class QuestionBlock(Tile):
    def __init__(self, x, y, itemtype: str):
        super().__init__(x, y)
        # string for the type of the object that stores the questionblock. "mushroom" for Mushroom
        self.__itemtype = itemtype
        self.__used = False
        self._used_block_image = Image(80, 0, 16, 16, 0)
        question_frames = []
        for i in range(5):
            question_frames.append(Image(i*16, 0, 16, 16, 0))
        self._animation = Animation(question_frames, FPS/4)

    def use(self):
        self.__used = True

    @property
    def used(self):
        return self.__used

    def get_item(self) -> Item:
        if self.__itemtype == "mushroom":
            return Mushroom(self.x, self.y - ITEM_SIZE, 1)

    def update(self):
        self._animation.update()

    def draw(self, x_shift: int):
        if self.__used:
            # draw used question block image
            self._used_block_image.draw(self.x + x_shift, self.y)
        else:
            # draw question block image
            self._animation.draw(self.x + x_shift, self.y)


class Floor(Tile):
    def __init__(self, x, y):
        # width and height of floor is 16
        super().__init__(x, y)
        self._floor_image = Image(32, 16, 16, 16, 0)

    def draw(self, x_shift: int):
        self._floor_image.draw(self.x + x_shift, self.y)


class Pipe(Tile):
    def __init__(self, x, y, orientation=0):
        # @param orientation
        # 0: upper left
        # 1: upper right
        # 2: bottom right
        # 3: bottom left
        super().__init__(x, y)
        self.__orientation = orientation

    def draw(self, x_shift):
        # depending on the orientation of the pipe, a different image is drawn
        if self.__orientation == 0:
            pyxel.blt(self.x + x_shift, self.y, 0, 0, 32, 16, 16, 12)
        elif self.__orientation == 1:
            pyxel.blt(self.x + x_shift, self.y, 0, 16, 32, 16, 16, 12)
        elif self.__orientation == 2:
            pyxel.blt(self.x + x_shift, self.y, 0, 16, 48, 16, 16, 12)
        elif self.__orientation == 3:
            pyxel.blt(self.x + x_shift, self.y, 0, 0, 48, 16, 16, 12)


class FlagPole(Tile):
    # flag pole
    def __init__(self, x, y):
        super().__init__(x, y)
        self._flag_pole_image = Image(80, 128, 16, 16, 0)

    def draw(self, x_shift):
        self._flag_pole_image.draw(self.x + x_shift, self.y)


class FlagTip(Tile):
    # tip of the flag
    def __init__(self, x, y):
        super().__init__(x, y)
        self._flag_tip_image = Image(80, 112, 16, 16, 0)

    def draw(self, x_shift):
        self._flag_tip_image.draw(self.x + x_shift, self.y)


class FinishFlag(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._finish_flag_image = Image(80, 96, 16, 16, 0)

    def draw(self, x_shift):
        self._finish_flag_image.draw(self.x + x_shift, self.y)