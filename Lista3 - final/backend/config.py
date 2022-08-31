WIDTH = 800
HEIGHT = 800
ROWS = 8
COLS = 8
FIELD_SIZE = WIDTH/ROWS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (181, 101, 29)
LIGHT_RED = (150, 0, 0)
LIGHT_GOLD = (255, 223, 0)
DARK_GOLD = (153, 101, 21)
BLUE = (0, 0, 150)
LIGHT_BLUE = (173, 216, 230)
PAWN_PADDING = 10
PAWN_BORDER = 2

# BOT
# PLAYER

PLAYERS = ['BOT', 'BOT']
EVAS = [1, 2]
DEPTH = 3
ALPHA_BETA = True
#HEURISTICS - 1 - fields, 2 - pawns, other - fields + pawns
EVALUATE = 3
WEIGHT_FIELDS = 1
WEIGHT_PAWNS = 3
MOVES = 0
STARTING_COLOR = WHITE
WINNER = None

COUNTER = 0
FPS = 60
DELAY = 50