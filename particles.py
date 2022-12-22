import pyxel

from random import randint
from animation import Image, Animation
from settings import FPS
from settings import GRAVITY
from sprite import Sprite


class Particle(Sprite):
    """Defines a particle, which has a boolean to know
    if it is showing. Useful to make in game objects such as coins, score numbers and broken blocks
    that show on screen for a brief period of time
    """

    def __init__(self, x, y, width = 0, height = 0):
        # particles are sometimes generated on decimal coordinates, so we need to convert it to an integer type
        super().__init__(int(x), int(y), width, height)
        # False if the particle no longer shows, then must be deleted
        self._showing = True

    @property
    def showing(self):
        return self._showing

    @showing.setter
    def showing(self, showing):
        self._showing = showing


class ScoreText(Particle):
    """This class defines the text that shows when Mario gets score
    by getting a coin, an item or killing an enemy
    """

    def __init__(self, x, y, score: int):
        super().__init__(x, y, 0, 0)
        self._time_count = 0
        self._max_time = FPS
        self._score = score

    def update(self):
        if self._time_count >= self._max_time:
            self._showing = False
        else:
            # go up
            self.y -= 1
            self._time_count += 1

    def draw(self, x_shift):
        if self._showing:
            pyxel.text(self.x + x_shift, self.y, str(self._score), 7)


class Coin(Particle):
    """This class defines the coin that shows when Mario touches a normal block
    or a question block that gives coins
    """

    def __init__(self, x, y):
        # When defining the coordinates, 16 is subtracted from Y
        # since the particle appears on top of the given block coordinates
        # and not inside it
        # 8 is added to X since coins are 8 pixels width
        super().__init__(x + 4, y - 16, 8, 16)
        # useful to make coin jump and fall
        self._vy = -10
        # Particle will last for half a second

        self._coin_frames = []
        for i in range(3):
            self._coin_frames.append(Image(i * 8, 144, 8, 16, 0))
        self._animation = Animation(self._coin_frames, FPS / 5)

    def update(self):
        self._animation.update()
        if self._animation.played_once:
            self._showing = False
        else:
            # add velocity to y
            self.y += self._vy
            # add gravity acceleration
            self._vy += GRAVITY

    def draw(self, x_shift):
        if self._showing:
            self._animation.draw(self.x + x_shift, self.y)


class BrokenBlockParticles(Particle):
    """This class defines the 4 little brick particles that appear when Mario breaks a block
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self._particles = []
        # add the 4 particles
        for i in range(4):
            # 2 last particles start lower than the block
            if i >= 2:
                self._particles.append(BrokenBlockParticle(x, y+8, i))
            else:
                self._particles.append(BrokenBlockParticle(x, y, i))

    def update(self):
        for particle in self._particles:
            particle.update()

    def draw(self, x_shift):
        for particle in self._particles:
            particle.draw(x_shift)


class BrokenBlockParticle(Particle):
    """This class defines the little brick particle that appears when breaking a block,
    which can have these possible directions:
    0: upper left
    1: upper right
    2: bottom right
    3: bottom left
    """

    def __init__(self, x, y, direction):
        super().__init__(x, y)
        if type(direction) == int:
            # upper left
            if direction == 0:
                self._vx = -5
                self._vy = -7
            # upper right
            elif direction == 1:
                self._vx = 5
                self._vy = -7
            # bottom right
            elif direction == 2:
                self._vx = 5
                self._vy = -5
            # bottom left
            elif direction == 3:
                self._vx = -5
                self._vy = -5
            else:
                raise ValueError("Direction is not valid")
            self._direction = direction
        else:
            raise TypeError("Direction is not valid")
        self._time_count = 0
        self._max_time = FPS
        # broken block particle image
        self._image = Image(80, 24, 8, 8, 0)

    def update(self):
        if self._time_count >= self._max_time:
            self._showing = False
        else:
            self.x += self._vx
            self.y += self._vy
            self._vy += GRAVITY
            self._time_count += 1

    def draw(self, x_shift):
        if self._showing:
            flip_horizontally = False
            flip_vertically = False
            # if direction is right (upper or bottom)
            if self._direction == 1 or self._direction == 2:
                flip_horizontally = True
            # if direction is bottom (right or left)
            if self._direction == 2 or self._direction == 3:
                flip_vertically = True

            self._image.draw(self.x + x_shift, self.y, flip_horizontally, flip_vertically)


class Firework(Particle):
    """This class defines the fireworks that appear when Mario wins the level
    and is inside the castle
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        # useful to make firework jump and fall
        self._vy = randint(-6, -2)
        # random velocity for the x axis
        self._vx = randint(-10, 10)
        # Particle will last for half a second

        self._firework_frames = []
        for i in range(3):
            self._firework_frames.append(Image(32 + i * 16, 144, 16, 16, 0))
        self._animation = Animation(self._firework_frames, FPS / 10)

    def update(self):
        self._animation.update()
        if self._animation.played_once:
            self._showing = False
        else:
            # add velocity to x
            self.x += self._vx
            # add velocity to y
            self.y += self._vy

    def draw(self, x_shift):
        if self._showing:
            self._animation.draw(self.x + x_shift, self.y)