from js import (
    console,
    document,
    devicePixelRatio,
    CanvasRenderingContext2D as Context2d,
    requestAnimationFrame,
    Element,
    window,
    Image,
    addEventListener,
)
from pyodide.ffi import create_proxy
from pyodide.ffi.wrappers import add_event_listener

ctx = None
canvas_width = 0
canvas_height = 0
frame_count = 0
imageBank = [] # image bank of max length 3
loadedImages = 0
loading = True

KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40

KEY_B = 90

_pressedKeys = {
    KEY_LEFT: False, 
    KEY_UP: False, 
    KEY_RIGHT: False, 
    KEY_DOWN: False,
    KEY_B: False
}

def _handle_input(e):
    global _pressedKeys
    if e.type == "keydown":
        _pressedKeys[e.keyCode] = True
    elif e.type == "keyup":
        _pressedKeys[e.keyCode] = False

def init(width: int, height: int, canvas: Element):
    global ctx
    ctx = canvas.getContext("2d")

    ctx.mozImageSmoothingEnabled = False
    ctx.webkitImageSmoothingEnabled = False
    ctx.msImageSmoothingEnabled = False
    ctx.imageSmoothingEnabled = False

    canvas.style.width = f"{width}px"
    canvas.style.height = f"{height}px"

    canvas.width = width
    canvas.height = height

    global canvas_width
    canvas_width = width
    global canvas_height
    canvas_height = height

    ctx.clearRect(0, 0, width, height)

     #init input
    add_event_listener(
        document,
        "keydown",
        _handle_input
    )

    add_event_listener(
        document,
        "keyup",
        _handle_input
    )



# inputs
def btn(key: int):
    return _pressedKeys[key]
    
def handle_image_load(e):
    global loadedImages
    loadedImages += 1

def load_assets(assets: list):
    global imageBank
    for imageSrc in assets:
        image = document.createElement('img')
        image.src = imageSrc
        
        add_event_listener(image, "load", handle_image_load)
        imageBank.append(image)

def update():
    global frame_count
    frame_count += 1
    global loading
    if loadedImages >= 3:
        loading = False

def fillRect(x, y, width, height):
    ctx.fillStyle = '#0ff';
    ctx.fillRect(x, y, width, height)

def cls(col=0):
    ctx.clearRect(0, 0, canvas_width, canvas_height)

def blt(x, y, image_bank: int, _x, _y, width, height, transparent_col=0):
    if loading:
        return
    #x, y refer to the position on the screen to draw
    #_x, _y refer to the position of the image in the image bank

    #in javascript:
    #ctx.drawImage(image, sourceX, sourceY, sWidth, sHeight, destinationX, destinationY, dWidth, dHeight)
    ctx.save()

    if (width < 0) and (height < 0):
        #flip horizontally and vertically
        ctx.scale(-1, -1)
        ctx.drawImage(imageBank[image_bank], _x, _y, -width, -height, -x, -y, width, height)

    elif width < 0:
        #flip horizontally
        ctx.scale(-1, 1)
        ctx.drawImage(imageBank[image_bank], _x, _y, -width, height, -x, y, width, height)

    elif height < 0:
        #flip vertically
        ctx.scale(1, -1)
        ctx.drawImage(imageBank[image_bank], _x, _y, width, -height, x, -y, width, height)
    
    else:
        ctx.drawImage(imageBank[image_bank], _x, _y, width, height, x, y, width, height)

    ctx.restore()

    #pyxel.blt(x, y, self._image_bank, self._x, self._y, width, height, self._transparent_col)


def text(x, y, text: str, color):
    if(color == 7):
        ctx.fillStyle = '#fff'

    ctx.fillText(text, x, y);

def quit():
    pass

### to do transparent colors into transparent pixels
"""
var imgd = ctx.getImageData(0, 0, imageWidth, imageHeight),
    pix = imgd.data;

for (var i = 0, n = pix.length; i <n; i += 4) {
    var r = pix[i],
        g = pix[i+1],
        b = pix[i+2];

    if(g > 150){ 
        // If the green component value is higher than 150
        // make the pixel transparent because i+3 is the alpha component
        // values 0-255 work, 255 is solid
        pix[i + 3] = 0;
    }
}

ctx.putImageData(imgd, 0, 0);​
"""