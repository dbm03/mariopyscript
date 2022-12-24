from js import (
    requestAnimationFrame,
    console,
    document,
    devicePixelRatio,
    ImageData,
    Uint8ClampedArray,
    CanvasRenderingContext2D as Context2d,
    requestAnimationFrame,
    Element,
    window,
    setInterval,
)

from pyodide.ffi import create_proxy

import pyxel
from particles import Firework
from level import Level
import settings

class App:
    def __init__(self):
        canvasDOM = document.querySelector("#canvas")
        
        # initialize ctx
        pyxel.init(256, 200, canvasDOM)
        pyxel.load_assets(["/assets/tiles.png", "/assets/spritesheet_mario.png", "/assets/background_03.png"])
        
        self.level = Level(settings.level01)
        self.start_game()

    
    def start_game(self):
        pyxel.fillRect(0, 0, 256, 100)
        proxy = create_proxy(self.game_loop)
        interval_id = setInterval(proxy, 33, "a parameter");

        # ctx.drawImage(background, 0, 0)

    def game_loop(self, *args, **kwargs):
        #requestAnimationFrame(create_proxy(self.game_loop))
        self.update()
        self.draw()

    def update(self):
        pyxel.update()
        
        self.level.update()



    def draw(self):
        pyxel.cls()
        
        self.level.draw()

App()