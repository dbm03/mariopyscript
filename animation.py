import pyxel


class Image:
    """This class stores coordinates, size, and the index of the image bank of an image in order
    to be easily drawn.
    """

    def __init__(self, x, y, width, height, image_bank, transparent_col=12):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._transparent_col = transparent_col
        if type(image_bank) == int:
            # pyxel only has 3 image banks available, so the index must be between 0 and 2
            if 3 > image_bank >= 0:
                self._image_bank = image_bank

    def draw(self, x, y, flip_horizontally=False, flip_vertically=False):
        if flip_horizontally:
            # negative width
            width = -self._width
        else:
            width = self._width
        if flip_vertically:
            # negative height
            height = -self._height
        else:
            height = self._height

        # draw image
        pyxel.blt(x, y, self._image_bank, self._x, self._y, width, height, self._transparent_col)


class Animation:

    def __init__(self, frames: list = [], delay = 0):
        self._frames = frames
        self._current_frame = 0
        self._start_time = pyxel.frame_count
        self._delay = delay
        self._played_once = False

    def update(self):
        elapsed = pyxel.frame_count - self._start_time
        if elapsed > self._delay:
            self._current_frame += 1
            self._start_time = pyxel.frame_count
        if self._current_frame == len(self._frames):
            self._current_frame = 0
            self._played_once = True

    @property
    def played_once(self) -> bool:
        return self._played_once

    def set_frames(self, frames: list):
        self._frames = frames
        self._current_frame = 0
        self._start_time = pyxel.frame_count
        self._played_once = False

    def set_delay(self, delay: int):
        self._delay = delay

    def get_image(self) -> Image:
        return self._frames[self._current_frame]

    def draw(self, x: int, y: int, flip_horizontally=False):
        self._frames[self._current_frame].draw(x, y, flip_horizontally)