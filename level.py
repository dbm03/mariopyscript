import pyxel
import random

import settings
from animation import Image
from enemies import Goomba, KoopaTroopa
from items import Mushroom
from mario import Mario
from level_tiles import Floor, Block, Pipe, QuestionBlock, CoinBlock, StairBlock, FlagTip, FlagPole, FinishFlag
from particles import BrokenBlockParticles, Firework
from settings import TILE_SIZE
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from settings import STARTING_TIME
from settings import FPS
from sprite import Sprite


class Camera:
    def __init__(self, world_width: int):
        self._x = 0

        # used to avoid Mario going back to the left
        self._maximum_x = 0
        self._y = 0
        self._world_width = world_width

    def focus(self, target: Sprite):
        # used to avoid Mario going back to the left
        if self._x > self._maximum_x:
            self._maximum_x = self._x

        self._x = target.center_x - SCREEN_WIDTH / 2
        if self._x < self._maximum_x:
            self._x = self._maximum_x
        elif self._x > self._world_width - SCREEN_WIDTH:
            self._x = self._world_width - SCREEN_WIDTH

    @property
    def minimum_x_mario(self):
        return self._maximum_x

    @property
    def x_shift(self):
        # returns the amount that must be added to an element that is drawn
        return -self._x


class Background:

    def __init__(self):
        self._background_width = 256
        self._background_image = Image(0, 0, 256, 256, 2)
        self._background1_x = 0
        self._background2_x = self._background_width
        # tells if the background1 is located left or right from background2
        self._background1_left = True
        # multiplier that makes the background move slower
        self._parallax_scroll = 3
        self._change = 0

    def update(self, x_shift):
        divisor = -x_shift // (self._background_width * self._parallax_scroll)
        if divisor > self._change:
            if self._background1_left:
                self._background1_x = self._background2_x + self._background_width
                self._background1_left = False
            else:
                self._background2_x = self._background1_x + self._background_width
                self._background1_left = True
            self._change += 1

    def draw(self, x_shift: int):
        # first background image
        self._background_image.draw(int(self._background1_x + (x_shift / self._parallax_scroll)), -64)
        # second background image
        self._background_image.draw(int(self._background2_x + (x_shift / self._parallax_scroll)), -64)


class Level:
    def __init__(self, level: tuple):
        self.time = STARTING_TIME
        self.tiles = []
        self.enemies = []
        self.items = []
        self.particles = []
        self.world_width = len(level[0]) * TILE_SIZE
        self.level_data = level
        self.create_level(level)
        self.camera = Camera(self.world_width)
        self.background = Background()
        # Mario starts with 5 lives by default
        self.lives = 5
        self.gameover = False
        self.castle_image = Image(0,64,80,80,0)
        self.flag_image = Image(80,80,16,16,0)
        # flag y is at the top of the castle
        self.flag_y = 100

    def create_level(self, level: tuple):
        # player spawns at 0, 0 by default
        self.player = Mario(0, 0)
        for row_index in range(len(level)):
            row = level[row_index]
            for col_index in range(len(row)):
                # character for the tile being currently iterated
                char = row[col_index]
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                # player position in level string
                if char == 'P':
                    self.player = Mario(x, y)
                elif char == 'F':
                    floor = Floor(x, y)
                    self.tiles.append(floor)
                elif char == 'B':
                    block = Block(x, y, True)
                    self.tiles.append(block)
                # pipes
                elif char == '<':
                    pipe = Pipe(x, y, 0)
                    self.tiles.append(pipe)
                elif char == '>':
                    pipe = Pipe(x, y, 1)
                    self.tiles.append(pipe)
                elif char == '(':
                    pipe = Pipe(x, y, 3)
                    self.tiles.append(pipe)
                elif char == ')':
                    pipe = Pipe(x, y, 2)
                    self.tiles.append(pipe)
                # question blocks
                elif char == 'Q':
                    question_block = QuestionBlock(x, y, 'mushroom')
                    self.tiles.append(question_block)
                # block with coins
                elif char == 'C':
                    coin_block = CoinBlock(x, y, random.randint(1, 5))
                    self.tiles.append(coin_block)
                elif char == '■':
                    stair_block = StairBlock(x, y)
                    self.tiles.append(stair_block)
                elif char == 'º':
                    flag_tip = FlagTip(x, y)
                    self.tiles.append(flag_tip)
                elif char == '|':
                    flag_pole = FlagPole(x,y)
                    self.tiles.append(flag_pole)
                elif char == '/':
                    flag = FinishFlag(int(x+TILE_SIZE/2),y)
                    self.tiles.append(flag)

    def update(self):

            self.player.update(self.tiles, self.enemies, self.items, self.particles)

            self.camera.focus(self.player)
            self.background.update(self.camera.x_shift)

            # Make Mario not able to go backwards
            if self.player.x < self.camera.minimum_x_mario:
                self.player.x = self.camera.minimum_x_mario

            if self.player.action != "grow" and not self.player.finishing_on_pole and not self.player.dead:
                # generate enemies
                self.spawn_enemies()

                # update enemies
                # iterated backwards so we are able to remove elements while iterating
                for i in range(len(self.enemies) - 1, -1, -1):
                    self.enemies[i].update(self.tiles, self.enemies)
                    # make enemy disappear if very far from Mario(so new enemies can be generated)
                    if abs(self.player.x - self.enemies[i].x) > SCREEN_WIDTH * 2:
                        del self.enemies[i]
                    elif self.enemies[i].dead:
                        # ensure that dead animation has played once before deleting enemy
                        if self.enemies[i].animation_played_once:
                            print("Killed: ", self.enemies[i])
                            del self.enemies[i]

                # update time counter
                # if 1 second elapsed
                if pyxel.frame_count % FPS == 0:
                    # remove 1 second from the timer
                    self.time -= 1

                    # if time is out, Mario must die
                    if self.time <= 0:
                        self.player.die()
            elif self.player.finishing_inside_castle:
                if self.flag_y > 80:
                    self.flag_y -= 1
                if self.time > 0:
                    if pyxel.frame_count % 10 == 0:
                        self.particles.append(Firework(SCREEN_WIDTH/2 - self.camera.x_shift, self.flag_y))
                    self.player.score += 200
                    self.time -= 2
                else:
                    self.time = 0
            elif self.player.dead:
                if self.player.animation.played_once:
                    if self.lives > 0:
                        self.lives -= 1
                        self.reset_level()
                    else:
                        # quit the game if not enough lives
                        pyxel.quit()


            # update items
            # iterated backwards so we are able to remove elements while iterating
            for i in range(len(self.items) - 1, -1, -1):
                self.items[i].update(self.tiles)
                if self.items[i].used:
                    print("Destroyed: ", self.items[i])
                    del self.items[i]

            # update particles
            # iterated backwards so we are able to remove elements while iterating
            for i in range(len(self.particles) - 1, -1, -1):
                self.particles[i].update()
                if not self.particles[i].showing:
                    del self.particles[i]

            # remove broken tiles
            # iterated backwards so we are able to remove elements while iterating
            for i in range(len(self.tiles) - 1, -1, -1):
                self.tiles[i].update()
                if self.tiles[i].broken:
                    # add broken block particles
                    self.particles.append(BrokenBlockParticles(self.tiles[i].x, self.tiles[i].y))
                    del self.tiles[i]

    def reset_level(self):
        self.time = STARTING_TIME
        self.tiles = []
        self.enemies = []
        self.items = []
        self.particles = []
        self.create_level(self.level_data)
        self.camera = Camera(self.world_width)
        self.background = Background()

    def spawn_enemies(self):
        if len(self.enemies) < 4:
            if pyxel.frame_count % (FPS*5) == 0:
                # create a koopa troopa 25% probability
                if random.random() < 0.25:
                    self.enemies.append(KoopaTroopa(int(SCREEN_WIDTH - self.camera.x_shift), 0))
                else:
                    self.enemies.append(Goomba(int(SCREEN_WIDTH - self.camera.x_shift), 0))

    def draw(self):
        # clear background with a blue sky color
        pyxel.cls()
        # background image
        self.background.draw(self.camera.x_shift)

        # draw tiles
        for tile in self.tiles:
            tile.draw(self.camera.x_shift)

        # draw castle when level player has won level
        if self.player.finishing_on_pole:
            self.flag_image.draw(settings.WORLD_WIDTH - (8 * TILE_SIZE) + self.camera.x_shift, self.flag_y)
            # castle is drawn on top of the flag
            self.castle_image.draw(settings.WORLD_WIDTH-(10*TILE_SIZE)+self.camera.x_shift,TILE_SIZE*6)

            # if end animation has finished
            if self.time == 0 and self.player.finishing_inside_castle:
                pyxel.text(100,120,"Press 'ESC' to exit",7)

        # draw player
        self.player.draw(self.camera.x_shift)

        # draw enemies
        for enemy in self.enemies:
            enemy.draw(self.camera.x_shift)

        # draw items
        for item in self.items:
            item.draw(self.camera.x_shift)

        # draw particles
        for particle in self.particles:
            particle.draw(self.camera.x_shift)

        # HUD elements
        # draw score
        pyxel.text(8, 8, "MARIO", 7)
        pyxel.text(8, 16, str(self.player.score), 7)
        # draw coins
        pyxel.text(64, 8, "x" + str(self.player.coins), 7)
        pyxel.blt(48, 8, 0, 32, 32, -16, 16, 12)
        # draw time
        pyxel.text(SCREEN_WIDTH / 1.5, 8, "TIME:" + str(self.time), 7)
        pyxel.text(100, 8, "LIVES:" + str(self.lives), 7)

    # These following functions are NOT USED IN FINAL VERSION, DEBUGGING PURPOSES
    def add_block(self, x: int, y: int):
        self.tiles.append(Block(int(x - self.camera.x_shift), y, True))

    def add_goomba(self, x: int, y: int):
        self.enemies.append(Goomba(int(x - self.camera.x_shift), y))

    def add_koopah(self, x, y):
        self.enemies.append(KoopaTroopa(int(x - self.camera.x_shift), y))

    def add_mushroom(self, x, y):
        self.items.append(Mushroom(int(x - self.camera.x_shift), y, 1))

    def add_broken(self, x, y):
        self.particles.append(BrokenBlockParticles(int(x-self.camera.x_shift),y))

    def add_firework(self, x, y):
        self.particles.append(Firework(int(x-self.camera.x_shift),y))