# NumpadPalette

A Krita plugin that enables use of a RGB led numeric keyboard as palette browser.

Tested with [ckb-next](https://github.com/ckb-next/ckb-next) and a Corsair K95 RGB Platinum Keyboard only.

![Keyboard numpad with palette in RGB](images/keyboard.jpg)
![Associated palette](images/palette.png)

## Usage

When enabled, the plugin will show the colors of the top-left swatches of the current palette on the numeric keypad keys. Pressing a key will set the color on that key as foreground color. Holding `Shift` and pressing a key sets it as background color.

You can move around in the palette (change the offset) with `Alt-` and the numeric keypad arrow keys. `Alt-5` resets position to the top left.

For now, you'll need to push one of the keys to initially trigger the plugin, and to update after palette changes. These aren't detected automatically.

## Motivation

I have this fancy RGB keyboard for whatever reason, and wondered if there is a way to actually use it in a constructive way, and not just for silly gamer effects. One of my directions of thinking was "can I somehow use this for art tooling", and this idea came to mind. Switching to certain colors instantly can be useful for pixel art.

I'm not exactly convinced that this plugin is super useful, for example the definition of the RGB leds is only barely enough to recognize the palette colors. But it's an interesting experiment nevertheless.

## Setup

### Krita setup

Copy the or link `pykrita` and `actions` folder contents to your local krita resources (usually `~/.local/share/krita`). Enable the plugin and restart Krita.

### ckb-next setup

- Under 'Performance' tab, set 'Num lock:' to 'always off'. We won't use the numlock as numlock but as extra function key.
- Under 'Lighting', add a `pipe` animation:
    - Give it id `1` (socket `/tmp/ckbpipe001` is hardcoded at the moment).
    - Assign (only) the numeric keypad keys to it. If you can't assign numlock, see above.

### Keyboard mapping setup

Using this plugin requires setting up the following binding for numeric keypad keys in your window manager:

```
/-----\/----\/----\/----\
| F13 | F14 | F15 | F16 |
|     |     |     |     |
+-----+-----+-----+-----|
| F17 | F18 | F19 | F20 |
|     |     |     |     |
+-----+-----+-----+     |
| F21 | F22 | F23 |     |
|     |     |     |     |
+-----+-----+-----+-----|
| F24 | F25 | F26 | F27 |
|     |     |     |     |
+-----+-----+-----+     |
| F28       | F29 |     |
|           |     |     |
+-----+-----+-----+-----|
```

#### Why is this needed?

Qt (as of 5.15.3) doesn't understand shortcuts with `KeypadModifier`, which would be required to make this work directly. It will completely ignore them, and trigger the non-keypad shortcut instead (according to QTBUG-20191, it's supposedly fixed but I couldn't get it to work in any way).

There seems to be no way around this in a Krita plugin. Even directly adding a event filter to the canvas doesn't seem to work, it won't get the key events. There may be other hacks possible but I tried a lot. Even adding an event filter to QApplication didn't work 100%, existing shortcuts would still get priority sometimes, and it is awful for input lag when done in Python.

So, the alternative way to make sure nothing interferes, is to remap the numpad to otherwise unused keys that Qt understands. This even allows us to use numlock.

(another option that might possibly work is to lay a widget over the canvas that intercepts events like done in [kritaCellBasedSelection](https://github.com/vmedea/kritaCellBasedSelection), however, this is hard to do consistently and it might add input lag)

#### Could rebinding in ckb-next work?

Possibly. But it doesn't give enough `Fxx` keys to make it work. Also, it seems that if you assign something to say, `F13` at the evdev level, it will actually assign it to some `XF86Tools` key (and so on...), due to xkb mapping shenanigans.

Why is this all so exhausting? I wish I knew. What at first glance seemed easy, became an expedition through the guts of OS input handling. Sometimes it's as if we optimized this world to maximize the number of hidden traps in everything. I do not claim to be innocent in this.

#### X11

- Add the following to `~/.Xmodmap`:

```
! clear numlock modifier
clear mod2
! reassign numpad to F13..F29
keycode 77 = F13 F13 F13
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
```

- load with `xmodmap ~/.Xmodmap` (or log in again)
- debug with `xmodmap -pke`

#### Wayland


- Put in `~/.xkb/symbols/custom`:

```
xkb_symbols "custom" {
    include "pc+us+inet(evdev)"

    modifier_map Mod2 { };

    replace key <NMLK>   {      [ F13 ]       };
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
```

- For sway: in `~/.config/sway/config`, add:

```
input "type:keyboard" {
     # custom layout in ~/.xkb/symbols/custom
     xkb_layout "custom"
}
```

For other wayland compositors, you'll need to find how to change the xkb layout.

## Future ideas

- Automatically detect palette changes (hook into switching document, switching palette, changing a palette color... somehow. I don't think Krita has any official hooks for these but there's probably some Qt signals).

- Show the current foreground/background color on some other key.

- Add some UI feedback (mostly of current palette position).

- Could have a fifth palette row if we use the four media keys above the keypad too.

