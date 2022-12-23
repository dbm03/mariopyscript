import pyxel

from animation import Animation, Image
from entity import Entity
from settings import GRAVITY, MAX_ACCELERATION, FPS
from settings import SCREEN_HEIGHT
from level_tiles import Block
from settings import GOOMBA_SPEED, KOOPA_SPEED, KOOPA_AREA


class Enemy(Entity):

    def __init__(self, x, y, width, height, speed=0):
        super().__init__(x, y, width, height)
        # movement speed
        self._speed = speed
        self.animation = Animation()

    def update(self, tiles: list, enemies: list):
        # enemies list parameter will be required to have collisions between enemies
        # enemy dies if falls to the void
        if self.y > SCREEN_HEIGHT:
            self._dead = True

    def hit(self, direction=0):
        # enemy dies if hit by default
        self._dead = True

    def _check_horizontal_collisions(self, tiles):
        pass

    def _check_vertical_collisions(self, tiles):
        pass

    @property
    def does_damage(self):
        # returns True if the enemy can damage Mario when he touches it
        if self._dead:
            return False
        else:
            return True

    @property
    def animation_played_once(self):
        return self.animation.played_once


class Goomba(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16, GOOMBA_SPEED)
        walk_frames = []
        for i in range(2):
            walk_frames.append(Image(i * 16, 0, 16, 16, 1))

        self._dead_image = Image(32, 0, 16, 16, 1)

        self.animation.set_frames(walk_frames)
        self.animation.set_delay(FPS / 2)

    def update(self, tiles: list, enemies: list):
        super().update(tiles, enemies)
        self.animation.update()
        # goomba won't move if dying
        if not self._dead:
            # apply gravity
            self._vy += GRAVITY
            # limit gravity acceleration
            if self._vy > MAX_ACCELERATION:
                self._vy = MAX_ACCELERATION
            # if direction is left
            if self._direction == 0:
                self._vx = -self._speed
            # direction is right
            else:
                self._vx = self._speed

            # check collisions
            self.x += self._vx
            self._check_horizontal_collisions(tiles)
            self.y += self._vy
            self._check_vertical_collisions(tiles)
            self._check_other_enemy_collision(enemies)

    def _check_horizontal_collisions(self, tiles: list):
        # enemy will change direction when touching a block
        for tile in tiles:
            if super().intersects(tile):
                if self._direction == 0:
                    self.left = tile.right
                    self._direction = 1
                else:
                    self.right = tile.left
                    self._direction = 0

    def _check_vertical_collisions(self, tiles: list):
        for tile in tiles:
            if super().intersects(tile):
                if self._vy > 0:
                    self.bottom = tile.top
                    if isinstance(tile, Block):
                        # goomba gets killed if block below has been destroyed or block is bouncing
                        if tile.broken or tile.bouncing:
                            self.hit()
                else:
                    self.top = tile.bottom
                self._vy = 0

    def _check_other_enemy_collision(self, enemies: list):
        for enemy in enemies:
            # check that the enemy in the list that is iterated is not itself
            if enemy is not self:
                if self.intersects(enemy):
                    # goomba can be killed by koopa troopa when hidden in shell
                    if isinstance(enemy, KoopaTroopa) and enemy.hidden_in_shell and enemy.does_damage:
                        self.hit()

    def draw(self, x_shift):
        self.animation.draw(self.x + x_shift, self.y)

    def hit(self, direction=0):
        # overwritten method so dead animation is played
        self.animation.set_frames([self._dead_image])
        self._dead = True


class KoopaTroopa(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 24, KOOPA_SPEED)
        self._hidden_in_shell = False
        # used to make koopa walk left and right continuously between two points
        self._initx = x
        self._walkarea = KOOPA_AREA
        self._shell_moving = False
        self._shell_speed = 6
        self._walk_frames = []
        for i in range(2):
            self._walk_frames.append(Image(i * 16, 16, 16, 24, 1))
        self._shell_frame = Image(32, 24, 16, 16, 1)
        self.animation.set_frames(self._walk_frames)
        self.animation.set_delay(FPS / 2)

    def update(self, tiles: list, enemies: list):
        super().update(tiles, enemies)
        self.animation.update()
        # apply gravity
        self._vy += GRAVITY
        # limit gravity acceleration
        if self._vy > MAX_ACCELERATION:
            self._vy = MAX_ACCELERATION

        # koopa moves when not hidden in shell
        if not self._hidden_in_shell:
            # change direction when koopa has walked for walkarea distance
            if abs(self._initx - self.x) > self._walkarea:
                if self._direction == 0:
                    self._direction = 1
                else:
                    self._direction = 0

            # if direction is left
            if self._direction == 0:
                self._vx = -self._speed
            # if direction is right
            else:
                self._vx = self._speed
        else:
            if self._shell_moving:
                # if direction is left
                if self._direction == 0:
                    self._vx = -self._shell_speed
                # if direction is right
                else:
                    self._vx = self._shell_speed
            else:
                self._vx = 0

        # check collisions
        self.x += self._vx
        self._check_horizontal_collisions(tiles)
        self.y += self._vy
        self._check_vertical_collisions(tiles)

    def _check_horizontal_collisions(self, tiles: list):
        for tile in tiles:
            if super().intersects(tile):
                if self._direction == 0:
                    self.left = tile.right
                    self._direction = 1
                else:
                    self.right = tile.left
                    self._direction = 0
                if isinstance(tile, Block):
                    if self._hidden_in_shell and self._shell_moving and tile.breakable:
                        tile.destroy()

    def _check_vertical_collisions(self, tiles: list):
        for tile in tiles:
            if super().intersects(tile):
                if self._vy > 0:
                    self.bottom = tile.top
                else:
                    self.top = tile.bottom
                self._vy = 0

    def hit(self, direction: int = 0):
        # @param direction 0 is left, 1 is right

        # Koopa already hidden in shell, shell moves when hit by Mario
        if self._hidden_in_shell:
            # toggle/untoggle shell moving
            self._shell_moving = not self._shell_moving
            self._direction = direction

        # Koopa hides in shell when hit for the first time
        else:
            self._hidden_in_shell = True
            self._vx = 0
            # Sprite height is not reduced when changing the form(walking or hidden in shell)
            # of the koopa since it can cause problems with collisions when there are
            # multiple koopas on the same spot:
            # when mario jumps on top of a shell(16 pixel height) he might get hit by
            # another koopa because it is 24 pixels tall

    def draw(self, x_shift):
        if self._hidden_in_shell:
            # must add 8 pixels to y coordinate so the shell(16x16 image) is on the ground and not floating
            self._shell_frame.draw(self.x + x_shift, self.y + 8)
        else:
            if self._direction == 0:
                # draw looking left
                self.animation.draw(self.x + x_shift, self.y)
            else:
                # draw looking right
                self.animation.draw(self.x + x_shift, self.y, True)

    @property
    def does_damage(self):
        # Returns True if Koopa can do damage to Mario when touched
        if self._hidden_in_shell:
            # if the koopa shell is moving
            if abs(self._vx) > 0 or abs(self._vy) > 0:
                return True
            else:
                return False
        else:
            return True

    @property
    def hidden_in_shell(self):
        return self._hidden_in_shell
