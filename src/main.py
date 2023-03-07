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

keyboard = KMKKeyboard()

keyboard.debug_enabled = False

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())

one_shot = OneShot()
keyboard.modules.append(one_shot)

pmw3360 = PMW3360(cs=board.D10, miso=board.MISO, mosi=board.MOSI, sclk=board.SCK, invert_x=True, invert_y=True, flip_xy=True)
# if str(getmount('/').label).endswith('R'):
keyboard.modules.append(pmw3360)

modtap = ModTap()
keyboard.modules.append(modtap)

split = Split(
    data_pin=board.RX,
    data_pin2=board.TX,
    # split_target_left=True,
    # uart_flip=True,
    use_pio=True,
    split_flip=False
)

keyboard.modules.append(split)

keyboard.extensions.append(MediaKeys())


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

# keyboard.keymap = [
#     [# BASE
#         KC.ESC,    KC.Q,       KC.W,       KC.E,       KC.R,       KC.T,                                 KC.Y,       KC.U,       KC.I,       KC.O,       KC.P,       KC.BSPC,
#         KC.TAB,    KC.A,       KC.S,       KC.D,       KC.F,       KC.G,                                KC.H,       KC.J,       KC.K,       KC.L,       KC.EQL,     DELRAL,
#         KC.LSFT,   KC.Z,       KC.X,       KC.C,       KC.V,       KC.B,                              KC.N,       KC.M,       KC.SCLN,    WSLFT,      WSLRT,
#         KC.LCTL,   KC.LALT,    CTLLSH,     SPCFN1,                    INSALT,       ENTF1,      RCTLQT,     KC.LCMD,
#                                                                     KC.VOLU,    KC.VOLD,              KC.MW_UP,     KC.MW_DN,
#                                                                                 KC.MUTE,              KC.MW_UP,
#     ]
# ]

keyboard.keymap = [
    [# BASE
        KC.ESC,  KC.N1,    KC.N2,   KC.N3, KC.N4, KC.N5,            KC.N6, KC.N7, KC.N8,   KC.N9,  KC.N0,   KC.BSPC,
        KC.TAB,  KC.Q,     KC.W,    KC.E,  KC.R,  KC.T,             KC.Y,  KC.U,  KC.I,    KC.O,   KC.P,    KC.MINS,
        KC.LSFT, KC.A,     KC.S,    KC.D,  KC.F,  KC.G,             KC.H,  KC.J,  KC.K,    KC.L,   KC.SCLN, KC.QUOT,
        KC.LCTL, KC.Z,     KC.X,    KC.C,  KC.V,  KC.B,             KC.N,  KC.M,  KC.COMM, KC.DOT, KC.SLSH, KC.BSLASH,
                           KC.LBRC, KC.RBRC,  KC.SPC, KC.SPC,    KC.ENT, KC.ENT,    KC.PLUS, KC.EQL,
                                              KC.TAB, KC.HOME,  KC.END, KC.DEL,
                                              KC.BSPC, KC.GRV,  KC.LGUI, KC.LALT
    ]
]

if __name__ == '__main__':
    print("starting")
    keyboard.go()
