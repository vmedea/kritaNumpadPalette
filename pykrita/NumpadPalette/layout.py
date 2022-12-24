# Layout -----------------
#
# /-----\/----\/----\/----\
# | -   | F13 | F14 | F15 |
# |     |     |     |     |
# +-----+-----+-----+-----|
# | F16 | F17 | F18 | F19 |
# |     |     |     |     |
# +-----+-----+-----+     |
# | F20 | F21 | F22 |     |
# |     |     |     |     |
# +-----+-----+-----+-----|
# | F23 | F24 | F25 | F26 |
# |     |     |     |     |
# +-----+-----+-----+     |
# | F27       | F28 |     |
# |           |     |     |
# +-----+-----+-----+-----|

# Qt key to ckb-next key.
BINDING = [
    ('F13', 'numlock'),
    ('F14', 'numslash'),
    ('F15', 'numstar'),
    ('F16', 'numminus'),
    ('F17', 'num7'),
    ('F18', 'num8'),
    ('F19', 'num9'),
    ('F20', 'numplus'),
    ('F21', 'num4'),
    ('F22', 'num5'),
    ('F23', 'num6'),
    ('F24', 'num1'),
    ('F25', 'num2'),
    ('F26', 'num3'),
    ('F27', 'numenter'),
    ('F28', 'num0'),
    ('F29', 'numdot'),
]

# ckb-next key to palette position.
KEYS = [
    ('numlock',  (0, 0)),   # scancode 77  NMLK
    ('numslash', (1, 0)),   # scancode 106 KPDV
    ('numstar',  (2, 0)),   # scancode 63  KPMU
    ('numminus', (3, 0)),   # scancode 82  KPSU
    ('num7',     (0, 1)),   # scancode 79  KP7
    ('num8',     (1, 1)),   # scancode 80  KP8
    ('num9',     (2, 1)),   # scancode 81  KP9
    ('numplus',  (3, 2)),   # scancode 86  KPAD
    ('num4',     (0, 2)),   # scancode 83  KP4
    ('num5',     (1, 2)),   # scancode 84  KP5
    ('num6',     (2, 2)),   # scancode 85  KP6
    ('num1',     (0, 3)),   # scancode 87  KP1
    ('num2',     (1, 3)),   # scancode 88  KP2
    ('num3',     (2, 3)),   # scancode 89  KP3
    ('numenter', (3, 4)),   # scancode 104 KPEN
    ('num0',     (0, 4)),   # scancode 90  KP0
    ('numdot',   (2, 4)),   # scancode 91  KPDL
]

# ckb-next key to movement direction.
MOVEMENT = [
    ('num7', 'UpLeft',    (-1, -1)),
    ('num8', 'Up',        ( 0, -1)),
    ('num9', 'UpRight',   ( 1, -1)),
    ('num4', 'Left',      (-1,  0)),
    ('num5', 'Reset',     None),
    ('num6', 'Right',     ( 1,  0)),
    ('num1', 'DownLeft',  (-1,  1)),
    ('num2', 'Down',      ( 0,  1)),
    ('num3', 'DownRight', ( 1,  1)),
]

# load with xmodmap ~/.Xmodmap
# debug with xmodmap -pke
XMODMAP = '''
keycode 106 = F14 F14 F14
keycode 63 = F15 F15 F15
keycode 82 = F16 F16 F16
keycode 79 = F17 F17 F17
keycode 80 = F18 F18 F18
keycode 81 = F19 F19 F19
keycode 86 = F20 F20 F20
keycode 83 = F21 F21 F21
keycode 84 = F22 F22 F22
keycode 85 = F23 F23 F23
keycode 87 = F24 F24 F24
keycode 88 = F25 F25 F25
keycode 89 = F26 F26 F26
keycode 104 = F27 F27 F27
keycode 90 = F28 F28 F28
keycode 91 = F29 F29 F29
'''

# put in ~/.xkb/symbols/custom
# sway config:
#   input "type:keyboard" {
#      # custom layout in ~/.xkb/symbols/custom
#      xkb_layout "custom"
#   }
XKB_CONFIG = '''
xkb_symbols "custom" {
    include "pc+us"

    replace key <KPDV>   {      [ F14 ]       };
    replace key <KPMU>   {      [ F15 ]       };
    replace key <KPSU>   {      [ F16 ]       };
    replace key <KP7>    {      [ F17 ]       };
    replace key <KP8>    {      [ F18 ]       };
    replace key <KP9>    {      [ F19 ]       };
    replace key <KPAD>   {      [ F20 ]       };
    replace key <KP4>    {      [ F21 ]       };
    replace key <KP5>    {      [ F22 ]       };
    replace key <KP6>    {      [ F23 ]       };
    replace key <KP1>    {      [ F24 ]       };
    replace key <KP2>    {      [ F25 ]       };
    replace key <KP3>    {      [ F26 ]       };
    replace key <KPEN>   {      [ F27 ]       };
    replace key <KP0>    {      [ F28 ]       };
    replace key <KPDL>   {      [ F29 ]       };
};
'''
