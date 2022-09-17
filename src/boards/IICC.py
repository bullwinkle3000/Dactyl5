import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.keypad import KeysScanner

class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8)
    row_pins = (board.GP9, board.GP10, board.GP11, board.GP12)
    diode_orientation = DiodeOrientation.COL2ROW 

    matrix = [MatrixScanner(col_pins, row_pins, diode_orientation), RotaryioEncoder(board.GP14, board.GP15), KeysScanner([board.GP13])]
    
    #debug_enabled = True;

    coord_mapping = [
        6,  5,  4,  3,  2,  1,  0,      32, 33, 34, 35, 36, 37,
        13, 12, 11, 10, 9,  8,  7,      39, 40, 41, 42, 43, 44,
            19, 18, 17, 16, 15, 14,     46, 47, 48, 49, 50,
                    24, 23, 22, 21,     52, 53, 54, 55,
                            29, 28,     59, 60,
                                30,     61,
    ]
 

