

class Sprite:
    '''contains coordinates for every object
    	that is displayed in the game'''

    def __init__(self, x, y, width: int, height: int):
        if type(x) == int and type(y) == int and type(width) == int and type(height) == int:
            self.x = x
            self.y = y
            self.width = width
            self.height = height
        else:
            raise TypeError("The type of the parameters is not valid")

    def update(self):
        pass

    def draw(self, x_shift):
        pass

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, bottom: int):
        self.y = bottom - self.height

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, right: int):
        if type(right) == int:
            self.x = right - self.width

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, left: int):
        if type(left) == int:
            self.x = left

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, top: int):
        if type(top) == int:
            self.y = top

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @center_x.setter
    def center_x(self, center_x: int):
        if type(center_x) == int or type(center_x) == float:
            self.x = center_x - self.width / 2

    @center_y.setter
    def center_y(self, center_y):
        if type(center_y) == int:
            self.y = center_y - self.height / 2

    def intersects(self, sprite):
        if isinstance(sprite, Sprite):
            return self.left < sprite.right and\
                   self.right > sprite.left and\
                   self.top < sprite.bottom and\
                   self.bottom > sprite.top
        else:
            raise TypeError("Type of intersect parameter is not a sprite")
