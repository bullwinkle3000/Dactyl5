import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.keypad import KeysScanner

class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.D2, board.D3, board.D4, board.D5, board.D6, board.D7)
    row_pins = (board.D8, board.D9, board.A3, board.A2, board.A1, board.A0)
    diode_orientation = DiodeOrientation.COL2ROW

    matrix = [MatrixScanner(col_pins, row_pins, diode_orientation)]

    debug_enabled = False

    # 5x6
    coord_mapping = [
        5,  4,  3,  2,  1,  0,      38, 39, 40, 41, 42, 43,
        11, 10, 9,  8,  7,  6,      44, 45, 46, 47, 48, 49,
        17, 16, 15, 14, 13, 12,     50, 51, 52, 53, 54, 55,
        23, 22, 21, 20, 19, 18,     56, 57, 58, 59, 60, 61,
                27, 26, 25, 24,     62, 63, 64, 65,
                        31, 30,     68, 69,
                        37, 36,     74, 75
    ]


