# macropad

Code for my macropad. I put Kailh navy switches on mine! Long live the click!

Modes:

- RGB config
- Numpad
- Media controls

## Setup

Adafruit's
[getting started guide](https://learn.adafruit.com/adafruit-macropad-rp2040) is
thorough but a bit verbose if this ain't your first rodeo. The TLDR:

### install circuitpython on the macropad

- Download the latest CircuitPython that will work with Macropad
  [here](https://circuitpython.org/board/adafruit_macropad_rp2040/).
- Enter the macropad bootloader by hoding down the rotary encoder and then
  clicking the reset button (on the left side)
- Extract the zip and drag the UF2 file into the Macropad folder
- The bootloader drive will die and be reborn as a drive called `CIRCUITPY`
- Now you can edit the code, in `code.py`!

### set up editor

I used this
[VSCode extension](https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython)
instead of the Mu editor. It has a serial monitor and auto-updates on save.

Download the adafruit circuitpython bundle
[here](https://circuitpython.org/libraries). You will need the following
libraries:

- `adafruit_macropad.mpy` - A helper library for using the features of the
  Adafruit MacroPad.
- `adafruit_debouncer.mpy` - A helper library for debouncing pins. Used to
  provide a debounced instance of the rotary encoder switch.
- `adafruit_simple_text_display.mpy` - A helper library for easily displaying
  lines of text on a display.
- `neopixel.mpy` - A CircuitPython driver for NeoPixel LEDs.
- `adafruit_display_text/` - A library to display text using displayio. Used for
  the text display functionality of the MacroPad library that allows you easily
  display lines of text on the built-in display.
- `adafruit_hid/` - CircuitPython USB HID drivers.
- `adafruit_midi/` - A CircuitPython helper for encoding/decoding MIDI packets
  over a MIDI or UART connection
- `adafruit_ticks.mpy` - A helper to work with intervals and deadlines in
  milliseconds
