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
)

from pyodide.ffi import create_proxy

import pyxel
from particles import Firework

class App:
    def __init__(self):
        canvasDOM = document.querySelector("#canvas")
        
        # initialize ctx
        pyxel.init(256, 200, canvasDOM)
        pyxel.load_assets(["/assets/tiles.png", "/assets/spritesheet_mario.png", "/assets/background_03.png"])
        
        print(pyxel)
        self.fireworks = []
        self.fireworks.append(Firework(50, 150))
        self.start_game()

    
    def start_game(self):
        # ctx.fillStyle = '#ccc'
        # ctx.fillRect(0,0,256,200)
        # ctx.fillStyle = '#0ff'
        # print("HOLA")
        # ctx.fillRect(0, 50, 100, 60)
        pyxel.fillRect(0, 50, 100, 100)
        self.game_loop()
        # ctx.drawImage(background, 0, 0)

    def game_loop(self, *args, **kwargs):
        requestAnimationFrame(create_proxy(self.game_loop))
        self.update()
        self.draw()

    def update(self):
        pyxel.update()
        if pyxel.frame_count % 10 == 0:
            self.fireworks.append(Firework(50,150))
        for firework in self.fireworks:
            firework.update()

        print(len(self.fireworks))


    def draw(self):
        pyxel.clear()
        pyxel.blt(0, 0, 2, 0, 0, 256, 256)
        for firework in self.fireworks:
            firework.draw(0)

App()