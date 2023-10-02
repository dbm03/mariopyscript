import pyxel

import settings
from animation import Animation, Image
from level_tiles import Block, QuestionBlock, CoinBlock, FinishFlag, FlagPole, FlagTip
from enemies import KoopaTroopa
from entity import Entity
from items import Mushroom
from particles import ScoreText, Coin
from settings import GRAVITY, MAX_ACCELERATION, FPS, WORLD_WIDTH


class Mario(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.can_jump = False
        self._speed = 4
        self.jump_force = 12
        # Direction of Mario, 0 stands for left; 1 stands for right
        self.score = 0
        self.coins = 0

        self.big = False

        self.invulnerable = False
        self.invulnerable_count = 0
        # mario stays invulnerable for 2 seconds after being hit
        self.invulnerable_time = settings.FPS * 2

        # by default, Mario starts with "stand"
        """These are the available action texts, used to specify
        which animation of Mario has to be played:
        'stand', jump', 'walk', 'grow', 'turn', 'shrink', 'death', 'grab'
        """
        self._current_action = "stand"
        # Load Mario animations
        self.__load_animations()

        # Win level variables
        # set to True when Mario is touching the finish flag pole
        self.finishing_on_pole = False
        # set to True when Mario is inside the castle( does not show anymore )
        self.finishing_inside_castle = False

        # used to calculate the points you get by landing on the flag pole
        self.landing_flag_pole_y = 0
        self.landing_score_added = False

    def __load_animations(self):
        """ This function creates variables that store Mario animations and images' coordinates
        on the sprite-sheet in order to draw them later
        """
        # small Mario animations/images
        self._dead_image = Image(96, 40, 16, 16, 1)
        self._small_walk_frames = []
        self._small_stand_image = Image(0, 40, 16, 16, 1)
        for i in range(3):
            self._small_walk_frames.append(Image(16 + i * 16, 40, 16, 16, 1))
        self._small_jump_image = Image(80, 40, 16, 16, 1)
        self._grow_frames = []
        for i in range(10):
            self._grow_frames.append(Image(i * 16, 88, 16, 32, 1))
        # image for when Mario changes direction
        self._small_turn_image = Image(64, 40, 16, 16, 1)
        self._small_grab_frames = []
        for i in range(2):
            self._small_grab_frames.append(Image(112 + i * 16, 40, 16, 16, 1))

        # big Mario animations/images
        self._big_stand_image = Image(0, 56, 16, 32, 1)
        self._big_jump_image = Image(80, 56, 16, 32, 1)
        self._big_walk_frames = []
        for i in range(3):
            self._big_walk_frames.append(Image(16 + i * 16, 56, 16, 32, 1))
        self._big_turn_image = Image(64, 56, 16, 32, 1)
        self._big_crouch_image = Image(96, 56, 16, 32, 1)
        self._big_grab_frames = []
        for i in range(2):
            self._big_grab_frames.append(Image(112 + i * 16, 56, 16, 32, 1))
        # starts with standing image
        self.animation = Animation()
        self.change_action("stand")

    def __apply_gravity(self):
        # Gravity
        self._vy += GRAVITY
        # Limit the gravity acceleration
        if self._vy > MAX_ACCELERATION:
            self._vy = MAX_ACCELERATION


    def update(self, tiles: list, enemies: list, items: list, particles: list):
        # since lists are mutable, we are able to change the objects lists in the level class
        # by changing these function parameters
        self.animation.update()
        if self.finishing_on_pole:
            # if Mario is touching the flag pole
            if (self.big and self.y < 128) or (not self.big and self.y - self.height < 128):
                if self._current_action != "grab":
                    self.change_action("grab")

                # mario goes down the flag pole
                self.y += 2
                self.__check_vertical_collisions(tiles, items, particles)
            else:
                # mario is at the bottom of the pole
                if not self.landing_score_added:
                    # y coordinate is inversely proportional to the points you get
                    # (the less Y the more points you get)
                    flag_score = 50000/self.landing_flag_pole_y
                    # approximate to hundreds
                    rounded_score = int(flag_score//100*100)
                    self.increase_score(rounded_score, particles)
                    self.landing_score_added = True
                self._direction = 0
                # move Mario to castle
                self.x += self._speed
                # if Mario is right of the pole
                if self.x >= WORLD_WIDTH - (settings.TILE_SIZE * 21):
                    self._direction = 1
                    # stick Mario on the ground
                    self.bottom = settings.TILE_SIZE * 11
                else:
                    self._direction = 0
                if self._current_action != "walk":
                    self.change_action("walk")

                self.__apply_gravity()
                self.y += self._vy
                self.__check_vertical_collisions(tiles, items, particles)
                if self.x >= WORLD_WIDTH - (settings.TILE_SIZE * 8):
                    # Mario is inside castle, finish level
                    self.finishing_inside_castle = True

        else:
            if self._current_action != "grow" and self._current_action != "death":
                if self.invulnerable:
                    self.invulnerable_count += 1
                    if self.invulnerable_count >= self.invulnerable_time:
                        self.invulnerable = False
                        self.invulnerable_count = 0

                self.__apply_gravity()

                if self.can_jump:
                    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_SPACE):
                        self._vy -= self.jump_force
                    # big mario can crouch
                    elif pyxel.btn(pyxel.KEY_DOWN) and self.big:
                        if self._current_action != "crouch":
                            self.change_action("crouch")
                    else:
                        if self._current_action == "jump":
                            # Mario is touching the ground after jumping
                            self.change_action("stand")
                else:
                    # cannot jump(then mario is falling)
                    if self._current_action != "jump":
                        # will show same image as jumping when falling
                        self.change_action("jump")

                # Mario movement
                self._vx = 0
                if pyxel.btn(pyxel.KEY_LEFT):
                    self._vx = -self._speed
                    self.__update_walk_animation(0)
                    self._direction = 0

                if pyxel.btn(pyxel.KEY_RIGHT):
                    self._vx = self._speed
                    self.__update_walk_animation(1)
                    self._direction = 1
                # if mario was walking/turning and he stopped
                if self._vx == 0 and (self._current_action == "walk" or self._current_action == "turn"):
                    self.change_action("stand")

                # Mario's movement and collisions
                self.x += self._vx
                self.__check_horizontal_collisions(tiles)
                self.__check_horizontal_enemies_collision(enemies)
                self.can_jump = False
                self.y += self._vy
                self.__check_vertical_collisions(tiles, items, particles)
                self.__check_vertical_enemies_collision(enemies, particles)

                # Collision with items
                self.__check_items_collision(items, particles)

                if self.x < 0:
                    self.x = 0
                if self.y > settings.SCREEN_HEIGHT:
                    self.die()
                if pyxel.btn(pyxel.KEY_B):
                    self._vy = -self.jump_force * 2
            
            if self._current_action == "grow":
                if self.animation.played_once:
                    self.change_action("stand")
            elif self._current_action == "death":
                self.__apply_gravity()
                # Mario jumps when dead
                self.y += self._vy

    def __update_walk_animation(self, new_direction: int):
        # if mario is not falling
        if self.can_jump:
            # if mario changed direction
            if self._direction != new_direction:
                self.change_action("turn")
            if self._current_action != "walk":
                if self._current_action == "turn":
                    # make sure that turn animation has been played once before changing into walking
                    if self.animation.played_once:
                        self.change_action("walk")
                else:
                    self.change_action("walk")

    def __check_horizontal_collisions(self, tiles: list):
        for tile in tiles:
            if super().intersects(tile):
                if self._direction == 0:
                    self.left = tile.right
                else:
                    if not self.finishing_on_pole:
                        if isinstance(tile, (FlagPole, FlagTip)):
                            self.landing_flag_pole_y = tile.y
                            self.center_x = tile.center_x
                            self.finishing_on_pole = True
                        elif isinstance(tile, FinishFlag):
                            pass
                        else:
                            self.right = tile.left
                    else:
                        if not isinstance(tile, (FlagPole, FinishFlag, FlagTip)):
                            self.right = tile.left

    def __check_vertical_collisions(self, tiles: list, items: list, particles: list):
        for i in range(len(tiles)):
            # if the rectangle of mario and tile overlap
            if super().intersects(tiles[i]):
                if isinstance(tiles[i], (FinishFlag, FlagTip, FlagPole)):
                    pass
                else:
                    # If Mario's velocity is positive, then he is touching ground
                    if self._vy > 0:
                        self.bottom = tiles[i].top
                        # Mario can jump because he is touching ground
                        self.can_jump = True

                    # hitting block with head
                    else:
                        self.top = tiles[i].bottom
                        # check if the tile is an instance of Block
                        if isinstance(tiles[i], Block):
                            # check if the block is breakable
                            if tiles[i].breakable:
                                # if mario is big block will be destroyed
                                if self.big:
                                    tiles[i].destroy()
                                # if mario is small block will bounce
                                else:
                                    tiles[i].bounce()
                        elif isinstance(tiles[i], QuestionBlock):
                            if not tiles[i].used:
                                # make sure that the question block can't be used again
                                tiles[i].use()
                                # if the item in the QuestionBlock is a Mushroom
                                if isinstance(tiles[i].get_item(), Mushroom):
                                    # just add a coin if Mario is already big
                                    if self.big:
                                        self.add_coin(tiles[i].x, tiles[i].y, particles)
                                        self.increase_score(100, particles)
                                    # create the Mushroom if Mario is small
                                    else:
                                        items.append(tiles[i].get_item())
                        elif isinstance(tiles[i], CoinBlock):
                            tiles[i].hit()
                            if tiles[i].gives_coins:
                                self.add_coin(tiles[i].x, tiles[i].y, particles)
                                self.increase_score(100, particles)
                    self._vy = 0

    def __check_horizontal_enemies_collision(self, enemies):
        for enemy in enemies:
            if self.intersects(enemy):
                if enemy.does_damage:
                    self.hit()
                else:
                    if isinstance(enemy, KoopaTroopa):
                        # hit koopa troopa shell horizontally when stopped
                        enemy.hit(self._direction)

    def __check_vertical_enemies_collision(self, enemies: list, particles: list):
        for enemy in enemies:
            if self.intersects(enemy):
                if self._vy > 0:
                    if not enemy.dead:
                        # bounce off the enemy
                        self.increase_score(100, particles)
                        self._vy = -self.jump_force / 1.2
                        self.bottom = enemy.top
                        if isinstance(enemy, KoopaTroopa):
                            # hit koopa troopa shell vertically
                            enemy.hit(self._direction)
                            if enemy.hidden_in_shell:
                                self.bottom = enemy.top
                        else:
                            enemy.hit()
                else:
                    if enemy.does_damage:
                        self.hit()

    def __check_items_collision(self, items: list, particles: list):
        for item in items:
            if isinstance(item, Mushroom):
                if self.intersects(item):
                    item.use()
                    self.__grow()
                    self.increase_score(1000, particles)

    def die(self):
        self._dead = True
        # make Mario jump when dead
        self._vy = -15
        self.change_action("death")

    def __grow(self):
        if not self.big:
            self.big = True
            self.y -= 16
            self.height = 32
            self.change_action("grow")

    def draw(self, x_shift):
        if not self.finishing_inside_castle:
            # when Mario is invulnerable, he is drawn half the time so a blinking effect is achieved
            if (self.invulnerable and pyxel.frame_count % 2 == 0) or not self.invulnerable:

                if self._direction == 0:
                    # mario is facing right in every image, so we need to flip images horizontally when direction is left
                    self.animation.draw(self.x + x_shift, self.y, flip_horizontally=True)
                else:
                    self.animation.draw(self.x + x_shift, self.y)

    def hit(self):
        if not self.invulnerable:
            # if Mario is big, survives
            if self.big:
                self.invulnerable = True
                # turn Mario small
                self.big = False
                self.y += 16
                self.height = 16
                self.change_action("stand")
            else:
                self.die()

    def add_coin(self, block_x, block_y, particles: list):
        self.coins += 1
        particles.append(Coin(block_x, block_y))

    def increase_score(self, points: int, particles: list):
        # Adds the given parameter points to the score of the player
        # and creates a ScoreText particle that will show the points that
        # the player just got
        self.score += points
        # draw points received on screen next to Mario
        particles.append(ScoreText(self.x, self.y, points))

    def change_action(self, new_action: str):
        """Changes the current action of Mario and sets the corresponding
        frames and delay between them for his animation object.
        :param new_action: The new action that Mario is doing
        """
        if type(new_action) == str:
            self._current_action = new_action
            if new_action == "stand":
                self.animation.set_delay(FPS / 6)
                if self.big:
                    self.animation.set_frames([self._big_stand_image])
                else:
                    self.animation.set_frames([self._small_stand_image])
            elif new_action == "walk":
                self.animation.set_delay(FPS / 6)
                if self.big:
                    self.animation.set_frames(self._big_walk_frames)
                else:
                    self.animation.set_frames(self._small_walk_frames)
            elif new_action == "turn":
                self.animation.set_delay(FPS / 6)
                if self.big:
                    self.animation.set_frames([self._big_turn_image])
                else:
                    self.animation.set_frames([self._small_turn_image])
            elif new_action == "jump":
                self.animation.set_delay(FPS / 6)
                if self.big:
                    self.animation.set_frames([self._big_jump_image])
                else:
                    self.animation.set_frames([self._small_jump_image])
            elif new_action == "grow":
                # can only grow when Mario is small
                self.animation.set_delay(FPS / 15)
                self.animation.set_frames(self._grow_frames)
            elif new_action == "crouch":
                # can only crouch when Mario is big
                self.animation.set_delay(FPS / 6)
                self.animation.set_frames([self._big_crouch_image])
            elif new_action == "grab":
                self.animation.set_delay(FPS / 6)
                if self.big:
                    self.animation.set_frames(self._big_grab_frames)
                else:
                    self.animation.set_frames(self._small_grab_frames)
            elif new_action == "death":
                # Mario can only die when small
                self.animation.set_delay(FPS)
                self.animation.set_frames([self._dead_image,self._dead_image,self._dead_image])
            else:
                # action does not exist
                raise ValueError("Action", new_action, "is not valid")

    @property
    def action(self):
        return self._current_action
