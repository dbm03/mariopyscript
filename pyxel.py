from js import (
    console,
    document,
    devicePixelRatio,
    CanvasRenderingContext2D as Context2d,
    requestAnimationFrame,
    Element,
    window,
    Image,
)
from pyodide.ffi import create_proxy

ctx = None
canvas_width = 0
canvas_height = 0
frame_count = 0
imageBank = []

def init(width: int, height: int, canvas: Element):
    print("Creating canvasss")
    global ctx
    ctx = canvas.getContext("2d")

    ctx.mozImageSmoothingEnabled = False;
    ctx.webkitImageSmoothingEnabled = False;
    ctx.msImageSmoothingEnabled = False;
    ctx.imageSmoothingEnabled = False;

    canvas.style.width = f"{width}px"
    canvas.style.height = f"{height}px"

    canvas.width = width
    canvas.height = height

    global canvas_width
    canvas_width = width
    print(width, canvas_width)
    global canvas_height
    canvas_height = height

    ctx.clearRect(0, 0, width, height)

def load_assets(assets: list):
    global imageBank
    for imageSrc in assets:
        image = document.createElement('img')
        image.src = imageSrc
        imageBank.append(image)
    
    print(imageBank)

def update():
    global frame_count
    frame_count += 1
    clear()

def fillRect(x, y, width, height):
    ctx.fillStyle = '#0ff';
    ctx.fillRect(x, y, width, height)

def clear():
    ctx.clearRect(0, 0, canvas_width, canvas_height)
    paintBg()

def blt(x, y, image_bank, width, height, transparent_col=0):
    pass

    #pyxel.blt(x, y, self._image_bank, self._x, self._y, width, height, self._transparent_col)

def paintBg():
    ctx.drawImage(imageBank[0], 0, 0);