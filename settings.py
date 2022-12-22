level01 = (
    '                                                                                                                                                                                                                            ',
    '                                                                                                                                                                                                     º                      ',
    '                                                                                                                                                                                                    /|                      ',
    '                                                                               BBBBBBBBBBBB   BBBQ                Q              BBB     BQQB                                                 ■■     |                      ',
    '                                                                                                                                                                                             ■■■     |                      ',
    '                     Q                                                                                                                                                                      ■■■■     |                      ',
    '                                                                                                                                                                                           ■■■■■     |                      ',
    '                                             <>         <>                  BQB                  C       BB     Q Q Q        S            CB      ■  ■          ■■  ■                     ■■■■■■     |                      ',
    '                   BQBQB             <>      ()         ()                                                                                       ■■  ■■        ■■■  ■■          QBB      ■■■■■■■     |                      ',
    '                           <>        ()      ()         ()                                                                                      ■■■  ■■■      ■■■■  ■■■     <>     <>   ■■■■■■■■     |                      ',
    '         P                 ()        ()      ()         ()                                                                                     ■■■■  ■■■■    ■■■■■  ■■■■    ()     ()  ■■■■■■■■■     ■         1             ',
    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  FFFFFFFFFFFFFFFFFF   FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  FFFFFFFFFFFFFFFFFF   FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
)
# Application settings
FPS = 30
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 200

# Level
STARTING_TIME = 500
TILE_SIZE = 16
# total width of the world in pixels
WORLD_WIDTH = len(level01[0])*TILE_SIZE
ITEM_SIZE = 16

# Gravity acceleration applied every frame
GRAVITY = 1
MAX_ACCELERATION = 10

# Enemies
GOOMBA_SPEED = 1
KOOPA_SPEED = 1
# fixed area where a koopa walks
KOOPA_AREA = 64
