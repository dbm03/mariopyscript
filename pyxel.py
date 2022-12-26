from js import (
    document,
    Element,
)
from pyodide.ffi.wrappers import add_event_listener

ctx = None
canvas_width = 0
canvas_height = 0
frame_count = 0
imageBank = [] # image bank of max length 3
loadedImages = 0
loading = True

_scale = 1

KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40

KEY_B = 66

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

def init(width: int, height: int, canvas: Element, scale: int = 1,):
    global ctx
    ctx = canvas.getContext("2d", {'alpha': False})

    ctx.mozImageSmoothingEnabled = False
    ctx.webkitImageSmoothingEnabled = False
    ctx.msImageSmoothingEnabled = False
    ctx.imageSmoothingEnabled = False

    canvas.style.width = f"{width*scale}px"
    canvas.style.height = f"{height*scale}px"

    canvas.width = width*scale
    canvas.height = height*scale

    global canvas_width
    canvas_width = width*scale
    global canvas_height
    canvas_height = height*scale

    global _scale
    _scale = scale

    ctx.clearRect(0, 0, width*scale, height*scale)

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
        ctx.drawImage(imageBank[image_bank], _x, _y, -width, -height, -x * _scale, -y * _scale, width*_scale, height*_scale)

    elif width < 0:
        #flip horizontally
        ctx.scale(-1, 1)
        ctx.drawImage(imageBank[image_bank], _x, _y, -width, height, -x * _scale, y * _scale, width*_scale, height*_scale)

    elif height < 0:
        #flip vertically
        ctx.scale(1, -1)
        ctx.drawImage(imageBank[image_bank], _x, _y, width, -height, x * _scale, -y * _scale, width*_scale, height*_scale)
    
    else:
        ctx.drawImage(imageBank[image_bank], _x, _y, width, height, x * _scale, y * _scale, width*_scale, height*_scale)

    ctx.restore()


def text(x, y, text: str, color):
    ctx.font = "10px Monospace"
    ctx.textAlign = 'left'
    if(color == 7):
        ctx.fillStyle = '#fff'

    ctx.fillText(text, x*_scale, y*_scale)

def centered_text(text: str, color):
    if color == 7:
        ctx.fillStyle = '#fff'

    ctx.textAlign = 'center'
    ctx.fillText(text, (canvas_width*_scale) / 2, (canvas_height*_scale) / 2)

def quit():
    pass
