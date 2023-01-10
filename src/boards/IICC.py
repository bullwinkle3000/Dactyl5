import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.keypad import KeysScanner

class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.D2, board.D3)
    row_pins = (board.D8, board.D9)
    diode_orientation = DiodeOrientation.COL2ROW

    matrix = [MatrixScanner(col_pins, row_pins, diode_orientation)]

    debug_enabled = False;

    coord_mapping = [
        6,  5,  4,  3,  2,  1,  0,      44, 45, 46, 47, 48, 49, 50,
        13, 12, 11, 10, 9,  8,  7,      51, 52, 53, 54, 55, 56, 57,
        20, 19, 18, 17, 16, 15, 14,     58, 59, 60, 61, 62, 63, 64,
        27, 26, 25, 24, 23, 22, 21,     65, 66, 67, 68, 68, 70, 71,
                    31, 30, 29, 28,     72, 73, 74, 75,
                            36, 35,     79, 80,
                            43, 42,     86, 87
    ]


