from adafruit_macropad import MacroPad


macropad = MacroPad()


last_position = 0
current_mode = 1
mode_select = False
brightness = 0.1
color = (100, 50, 150)

# NUM PAD

num_map = [
    macropad.Keycode.SEVEN,
    macropad.Keycode.EIGHT,
    macropad.Keycode.NINE,
    macropad.Keycode.FOUR,
    macropad.Keycode.FIVE,
    macropad.Keycode.SIX,
    macropad.Keycode.ONE,
    macropad.Keycode.TWO,
    macropad.Keycode.THREE,
    macropad.Keycode.ZERO,
    macropad.Keycode.ZERO,
    macropad.Keycode.ZERO,
]


def num_pad_view():
    text_lines = macropad.display_text(title="NUMPAD")

    text_lines[0].text = "7 8 9"
    text_lines[1].text = "4 5 6"
    text_lines[2].text = "1 2 3"
    text_lines[3].text = "0 0 0"

    text_lines.show()


def num_pad():
    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            macropad.keyboard.send(num_map[key_event.key_number])


# MODE SELECTION

def mode_select_view():
    text_lines = macropad.display_text(title="SELECT MODE")

    text_lines[0].text = "> {}".format(modes[current_mode]["title"])
    text_lines[1].text = "  {}".format(
        modes[(current_mode+1) % len(modes)]["title"])
    text_lines[2].text = "  {}".format(
        modes[(current_mode+2) % len(modes)]["title"])
    text_lines[3].text = "  {}".format(
        modes[(current_mode+3) % len(modes)]["title"])
    text_lines[4].text = "  {}".format(
        modes[(current_mode+4) % len(modes)]["title"])
    text_lines.show()


def select_mode():
    global current_mode
    global last_position

    encoder_pos = macropad.encoder
    if (encoder_pos > last_position):
        current_mode += 1
        current_mode %= len(modes)
        last_position = encoder_pos
        mode_select_view()

    if macropad.encoder < last_position:
        current_mode -= 1
        current_mode %= len(modes)
        last_position = encoder_pos
        mode_select_view()


# MEDIA CONTROLS

def media_view():
    disp = macropad.display_text(title="MEDIA")
    disp[0].text = "ddddd"
    disp[1].text = "green"
    disp[2].text = "bluedddd"

    disp.show()


def media_controls():
    global last_position

    encoder_pos = macropad.encoder

    if macropad.encoder > last_position:
        macropad.consumer_control.send(
            macropad.ConsumerControlCode.VOLUME_INCREMENT)
        last_position = encoder_pos

    if macropad.encoder < last_position:
        macropad.consumer_control.send(
            macropad.ConsumerControlCode.VOLUME_DECREMENT)
        last_position = encoder_pos

# RGB


def rgb_view():
    text_lines = macropad.display_text(title="RGB")

    text_lines[0].text = "Brightness {}".format(brightness)
    text_lines[1].text = "green"
    text_lines[2].text = "blue"

    text_lines.show()


def rgb():
    global last_position
    global brightness

    encoder_pos = macropad.encoder

    if macropad.encoder > last_position:
        brightness += 0.05
        last_position = encoder_pos
        rgb_view()

    if macropad.encoder < last_position:
        brightness -= 0.05
        last_position = encoder_pos
        rgb_view()

# MAIN LOOP


modes = [
    {"title": "RGB Crap", "func": rgb, "view": rgb_view},
    {"title": "Media Controls", "func": media_controls, "view": media_view},
    {"title": "Num Pad", "func": num_pad, "view": num_pad_view}
]


modes[current_mode]["view"]()

while True:
    if mode_select:
        select_mode()
    else:
        modes[current_mode]["func"]()

    macropad.pixels.brightness = brightness
    macropad.pixels.fill(color)

    # ENCODER LOGIC

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:
        mode_select = not mode_select

        if mode_select:
            mode_select_view()
        else:
            modes[current_mode]["view"]()
