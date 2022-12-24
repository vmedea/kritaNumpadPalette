#!/usr/bin/env python3
import os
import os.path
import sys

sys.path.append('pykrita/NumpadPalette')
import layout

target_path = 'actions'

def get_binding_for(keyname):
    for (assigned, key) in layout.BINDING:
        if key == keyname:
            return assigned
    return None

def create_action(name, text, shortcut):
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<ActionCollection version="2" name="Scripts">
    <Actions category="NumpadPalette">
        <text>NumpadPalette</text>

        <Action name="{name}">
        <icon></icon>
        <text>{text}</text>
        <whatsThis></whatsThis>
        <toolTip></toolTip>
        <iconText></iconText>
        <activationFlags>10000</activationFlags>
        <activationConditions>0</activationConditions>
        <shortcut>{shortcut}</shortcut>
        <isCheckable>false</isCheckable>
        <statusTip></statusTip>
        </Action>
    </Actions>
</ActionCollection>
'''

    with open(os.path.join(target_path, name) + ".action", "w") as f:
        f.write(xml)

for idx, key in enumerate(layout.KEYS):
    assigned = get_binding_for(key[0])
    for is_bg in range(2):
        shortcut = ''
        if is_bg == 0:
            name = 'NumpadPaletteFg' + str(idx)
            ground = 'foreground'
            if assigned is not None:
                shortcut = assigned
        else:
            name = 'NumpadPaletteBg' + str(idx)
            ground = 'background'
            if assigned is not None:
                shortcut = 'Shift+' + assigned
        text = f'Set {ground} to color {idx}'
        create_action(name, text, shortcut)

for idx, key in enumerate(layout.MOVEMENT):
    assigned = get_binding_for(key[0])
    name = 'NumpadPalette' + key[1]
    if assigned is not None:
        shortcut = 'Alt+' + assigned
    else:
        shortcut = ''
    text = f'Move color selection palette {key[1]}'
    create_action(name, text, shortcut)

