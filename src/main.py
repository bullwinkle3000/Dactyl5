import board
from storage import getmount

from kmk.boards.IICC import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.pmw3360 import PMW3360
from kmk.modules.oneshot import OneShot

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())

one_shot = OneShot()
keyboard.modules.append(one_shot)

pmw3360 = PMW3360(cs=board.GP17, miso=board.GP16, mosi=board.GP19, sclk=board.GP18, invert_x=True, invert_y=True, flip_xy=True)
if str(getmount('/').label).endswith('R'):
    keyboard.modules.append(pmw3360)

modtap = ModTap()
keyboard.modules.append(modtap)

split = Split(data_pin=board.GP1, data_pin2=board.GP0, uart_flip=False, split_flip=False)
keyboard.modules.append(split)

keyboard.extensions.append(MediaKeys())

rgb_ext = RGB(pixel_pin=board.GP28, num_pixels=18)
keyboard.extensions.append(rgb_ext)

layer_delay = 300

def ball_scroll_enable(key, keyboard, *args):
    pmw3360.start_v_scroll()
    return True

def ball_scroll_disable(key, keyboard, *args):
    pmw3360.start_v_scroll(False)
    return True

def ball_volume_enable(key, keyboard, *args):
    pmw3360.start_volume_control()
    return True

def ball_volume_disable(key, keyboard, *args):
    pmw3360.start_volume_control(False)
    return True

#chained keys
WSLFT = KC.LCMD(KC.LCTL(KC.LEFT))
WSLRT = KC.LCMD(KC.LCTL(KC.RIGHT))
CLSA = KC.LALT(KC.F4)
FARU = KC.LCTL(KC.PGUP)
FARL = KC.LALT(KC.F1)

#one shots
OLSFT = KC.OS(KC.LSFT)
ORCTL = KC.OS(KC.RCTL)
OLALT = KC.OS(KC.LALT)
OLCTL = KC.OS(KC.LCTL)

#Modtap
DELRAL = KC.MT(KC.DEL, KC.RALT)
INSALT = KC.MT(KC.INS, KC.LALT)
RCTLQT = KC.MT(KC.QUOT, KC.RCTL)
CTLLSH = KC.MT(KC.SLSH, KC.LCTL)


#Layer keys
SPCFN1 = KC.LT(1, KC.SPC, prefer_hold=True, tap_interrupted=False, tap_time=layer_delay)
TABFN2 = KC.LT(2, KC.TAB, prefer_hold=True, tap_interrupted=False, tap_time=layer_delay)
ENTF1 = KC.LT(1, KC.ENT, prefer_hold=True, tap_interrupted=False, tap_time=layer_delay)
ZMSB = KC.LT(3, KC.Z, prefer_hold=True, tap_interrupted=False, tap_time=layer_delay)

SPCFN1.before_press_handler(ball_volume_enable)
SPCFN1.before_release_handler(ball_volume_disable)
TABFN2.before_press_handler(ball_scroll_enable)
TABFN2.before_release_handler(ball_scroll_disable)

keyboard.keymap = [
    [# BASE
        KC.ESC,     KC.Q,       KC.W,       KC.E,       KC.R,       KC.T,       KC.MB_MMB,                          KC.Y,       KC.U,       KC.I,       KC.O,       KC.P,       KC.BSPC,
        KC.LSFT,    KC.A,       KC.S,       KC.D,       KC.F,       KC.G,       KC.MB_LMB,                          KC.H,       KC.J,       KC.K,       KC.L,       KC.EQL,     DELRAL,
                    ZMSB,       KC.X,       KC.C,       KC.V,       KC.B,       KC.MB_RMB,                          KC.N,       KC.M,       KC.SCLN,    WSLFT,      WSLRT,      
                                            KC.LALT,    CTLLSH,     SPCFN1,     TABFN2,               INSALT,       ENTF1,      RCTLQT,     KC.LCMD,
                                                                    KC.VOLU,    KC.VOLD,              KC.MW_UP,     KC.MW_DN,
                                                                                KC.MUTE,              KC.MB_BK,
    ],
    [# NUMBERS
        CLSA,       KC.N1,      KC.N2,      KC.N3,      KC.N4,      KC.N5,      KC.BSPC,                            KC.BSLS,    KC.LBRC,    KC.MINS,    KC.RBRC,    KC.GRV,     KC.TRNS,
        KC.TRNS,    KC.N6,      KC.N7,      KC.N8,      KC.N9,      KC.N0,      KC.DEL,                             KC.LEFT,    KC.DOWN,    KC.UP,      KC.RIGHT,   KC.TRNS,    KC.TRNS,
                    OLSFT,      ORCTL,      KC.MINS,    KC.COMM,    KC.DOT,     KC.PLUS,                            KC.COMM,    KC.DOT,     KC.TRNS,    KC.RGB_VAI, KC.RGB_VAD,      
                                            OLALT,      OLCTL,      KC.TRNS,    KC.TRNS,              KC.TRNS,      KC.TRNS,    KC.TRNS,    KC.TRNS,
                                                                    KC.RGB_HUI, KC.RGB_HUD,           KC.RGB_SAI,   KC.RGB_SAD,
                                                                                KC.TRNS,              KC.RGB_TOG,
    ],
    [# FN
        KC.PGUP,    KC.F1,      KC.F2,      KC.F3,      KC.F4,      KC.F5,      FARU,                               KC.MB_BK,   KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,
        KC.PGDN,    KC.F6,      KC.F7,      KC.F8,      KC.F9,      KC.F10,     KC.ENT,                             KC.HOME,    KC.PGDN,    KC.PGUP,    KC.END,     KC.TRNS,    KC.TRNS,
                    ZMSB,       WSLFT,      WSLRT,      KC.V,       KC.B,       FARL,                               KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,      
                                            KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,              KC.TRNS,      KC.TRNS,    KC.TRNS,    KC.TRNS,
                                                                    KC.TRNS,    KC.TRNS,              KC.TRNS,      KC.TRNS,
                                                                                KC.TRNS,              KC.MPLY,
    ],
    [# Mouse
        KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,                            KC.P7,    KC.P8,    KC.P9,    KC.PPLS,    KC.PMNS,    KC.TRNS,
        KC.CAPS,    KC.TRNS,    KC.LALT,    KC.LCTL,    KC.LSFT,    KC.EQL,     KC.TRNS,                            KC.P4,    KC.P5,    KC.P6,    KC.PAST,    KC.PSLS,    KC.TRNS,
                    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.TRNS,                            KC.P1,    KC.P2,    KC.P3,    KC.PEQL,    KC.NLCK,      
                                            KC.TRNS,    KC.MB_MMB,  KC.MB_LMB,  KC.MB_RMB,            KC.P0,        KC.PENT,  KC.PSCR,  KC.SLCK,
                                                                    KC.TRNS,    KC.TRNS,              KC.TRNS,      KC.TRNS,
                                                                                KC.TRNS,              KC.TRNS,
    ],
]

if __name__ == '__main__':
    keyboard.go()
