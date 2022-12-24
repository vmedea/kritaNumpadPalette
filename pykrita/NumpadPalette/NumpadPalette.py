from krita import *
import functools
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QErrorMessage

from .layout import KEYS, MOVEMENT

CKB_PIPE = '/tmp/ckbpipe001'

# For color setting, see
#    https://github.com/vmedea/ckb-next-integrations/blob/main/keyleds-ckb.vim
def keyboard_set(ckb_pipe, colors_in):
    '''
    Send a series of commands to ckb-next to change key RBGA colors.
    Colors must be in RRGGBBAA hexadecimal format.
    '''
    with open(ckb_pipe, 'w') as f:
        for (key, value) in colors_in.items():
            f.write('rgb ' + key + ':' + value + '\n')


def color_to_hex(color):
    color = color.components()
    return ''.join(f'%02x' % (min(max(int(color[i] * 256.0), 0), 255), ) for i in range(4))


def get_palette_size(palette):
    if palette is not None:
        return (palette.columnCount(), 100) # XXX height
    else:
        return (0, 0)

def get_current_palette(app):
    '''
    Get current palette from palette docker.
    '''
    for docker in app.dockers():
        if docker.metaObject().className() == 'PaletteDockerDock':
            widget = docker.widget()
            label = widget.findChild(QLabel, 'lblPaletteName')
            if label is None:
                return None
            palette_name = label.text()

            # Look up resource by name.
            resources = app.resources("palette")
            res = resources.get(palette_name, None)
            if res is not None:
                return Palette(res)
            else:
                return None

    return None

class NumpadPaletteExtension(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        # XXX should clear keyboard state on Krita startup and exit.
        self.reset()
        # XXX should detect when krita palette is ready before callign this,
        # otherwise app.dockers() crashes.
        #self.updateKeyboard()

    def reset(self):
        print('NumpadPalette: Reset')
        self.ofs = [0, 0]

    def getPalette(self):
        '''
        Get the configured palette as Krita object.
        '''
        # XXX detect when palette changed.
        return get_current_palette(Krita.instance())

    def getColor(self, palette, coord):
        '''
        Get a color from the palette, by coordinate.
        '''
        coord = [self.ofs[0] + coord[0], self.ofs[1] + coord[1]]
        if palette is None or coord[0] < 0 or coord[1] < 0 or coord[0] >= palette.columnCount():
            # Return solid black if no palette or out of range.
            color = ManagedColor("RGBA", "U8", "")
            color.setComponents([0.0, 0.0, 0.0, 1.0])
            return color

        index = coord[0] + coord[1] * palette.columnCount()
        return palette.colorSetEntryByIndex(index).color()

    def updateKeyboard(self):
        '''
        Update keyboard led colors from palette.
        '''
        palette = self.getPalette()

        to_set = {}
        for key in KEYS:
            to_set[key[0]] = color_to_hex(self.getColor(palette, key[1]))

        keyboard_set(CKB_PIPE, to_set)

    def choose(self, coord, is_bg):
        '''
        Sets the foreground/background color to a color from the palette, by coordinate.
        '''
        print("NumpadPalette: choose ", coord, is_bg)
        view = Krita.instance().activeWindow().activeView()
        palette = self.getPalette()
        if palette is None:
            em = QErrorMessage()
            em.showMessage(f"Could not find current palette. This is likely an incompoatibility of the plugin with the current version of krita.")
            em.exec_()
        else:
            color = self.getColor(palette, coord)
            print("NumpadPalette: color=", color.components())
            if is_bg:
                view.setBackGroundColor(color)
            else:
                view.setForeGroundColor(color)

        self.updateKeyboard() # Do this here (I don't know how to watch the palette for changes).

    def move(self, delta):
        if delta is None: # Special reset case.
            self.reset()
            self.updateKeyboard()
            return

        self.ofs = [self.ofs[0] + delta[0], self.ofs[1] + delta[1]]

        # Get width and height of current palette.
        dims = get_palette_size(self.getPalette())

        # Clipping.
        # There's an extra allowed border of 1 to make sure u can reach all colors.
        self.ofs[0] = min(max(self.ofs[0], -1), dims[0] + 1 - 4)
        self.ofs[1] = min(max(self.ofs[1], -1), dims[1] + 1 - 5)

        print(f'NumpadPalette: move {delta} to position {self.ofs}')

        self.updateKeyboard()

    def createActions(self, window):
        for n,key in enumerate(KEYS):
            name = "NumpadPaletteFg" + str(n)
            action = window.createAction(name, name, "")
            action.triggered.connect(functools.partial(self.choose, key[1], False))

            name = "NumpadPaletteBg" + str(n)
            action = window.createAction(name, name, "")
            action.triggered.connect(functools.partial(self.choose, key[1], True))

        for key in MOVEMENT:
            name = "NumpadPalette" + key[1]
            action = window.createAction(name, name, "")
            action.triggered.connect(functools.partial(self.move, key[2]))

#Adding extension to Krita's list of extensions
Krita.instance().addExtension(NumpadPaletteExtension(Krita.instance()))