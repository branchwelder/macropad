from adafruit_macropad import MacroPad

macropad = MacroPad()

state = {
    "last_position": 0,
    "mode": 1,
    "mode_select": False,
    "brightness": 0.1,
    "color": {
        "r": 250,
        "g": 35,
        "b": 0
    },
    "pressed_keys": set()
}

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


def num_pad(key_events):
    if key_events:
        if key_events.pressed:
            macropad.keyboard.send(num_map[key_events.key_number])


# MODE SELECTION

def mode_select_view():
    current_mode = state["mode"]
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
    encoder_pos = macropad.encoder
    if (encoder_pos > state["last_position"]):
        state["mode"] += 1
        state["mode"] %= len(modes)
        state["last_position"] = encoder_pos
        mode_select_view()

    if macropad.encoder < state["last_position"]:
        state["mode"] -= 1
        state["mode"] %= len(modes)
        state["last_position"] = encoder_pos
        mode_select_view()


# MEDIA CONTROLS

media_map = [
    234,  # previous track
    232,  # play/pause
    235,  # next track
    111,  # toggle mic
    239,  # toggle audio
    macropad.ConsumerControlCode.PLAY_PAUSE,
    123,  # cut
    124,  # copy
    125,  # paste
    macropad.ConsumerControlCode.PLAY_PAUSE,
    macropad.ConsumerControlCode.PLAY_PAUSE,
    macropad.ConsumerControlCode.PLAY_PAUSE,
]


def media_view():
    disp = macropad.display_text(title="MEDIA")
    disp[0].text = "prev play/pause next"
    disp[1].text = "mic mute ____"
    disp[2].text = "cut copy paste"
    disp[2].text = "____ ____ ____"

    disp.show()


def media_controls(key_events):
    encoder_pos = macropad.encoder

    if macropad.encoder > state["last_position"]:
        macropad.consumer_control.send(
            macropad.ConsumerControlCode.VOLUME_INCREMENT)
        state["last_position"] = encoder_pos

    if macropad.encoder < state["last_position"]:
        macropad.consumer_control.send(
            macropad.ConsumerControlCode.VOLUME_DECREMENT)
        state["last_position"] = encoder_pos

    if key_events:
        if key_events.pressed:
            macropad.keyboard.send(media_map[key_events.key_number])

# RGB


def rgb_view():
    text_lines = macropad.display_text(title="RGB")

    text_lines[0].text = "R {} - G {} - B{}".format(
        state["color"]["r"], state["color"]["g"], state["color"]["b"])
    text_lines[1].text = "Brightness {}".format(state["brightness"])

    text_lines.show()


def rgb(key_events):
    encoder_pos = macropad.encoder

    if macropad.encoder > state["last_position"]:
        state["last_position"] = encoder_pos
        if 0 in state["pressed_keys"]:
            state["color"]["r"] = (state["color"]["r"] + 10) % 255
        if 1 in state["pressed_keys"]:
            state["color"]["g"] = (state["color"]["g"] + 10) % 255
        if 2 in state["pressed_keys"]:
            state["color"]["b"] = (state["color"]["b"] + 10) % 255
        if 3 in state["pressed_keys"]:
            state["brightness"] = round((state["brightness"] + 0.02) % 1, 2)
        rgb_view()

    if macropad.encoder < state["last_position"]:
        if 0 in state["pressed_keys"]:
            state["color"]["r"] = (state["color"]["r"] - 10) % 255
        if 1 in state["pressed_keys"]:
            state["color"]["g"] = (state["color"]["g"] - 10) % 255
        if 2 in state["pressed_keys"]:
            state["color"]["b"] = (state["color"]["b"] - 10) % 255
        if 3 in state["pressed_keys"]:
            state["brightness"] = round((state["brightness"] - 0.02) % 1, 2)

        state["last_position"] = encoder_pos
        rgb_view()

# MAIN LOOP


modes = [
    {"title": "RGB Crap", "func": rgb, "view": rgb_view},
    {"title": "Media Controls", "func": media_controls, "view": media_view},
    {"title": "Num Pad", "func": num_pad, "view": num_pad_view}
]


modes[state["mode"]]["view"]()

while True:

    macropad.pixels.brightness = state["brightness"]
    macropad.pixels.fill(
        (state["color"]["r"], state["color"]["g"], state["color"]["b"]))

    key_events = macropad.keys.events.get()
    if key_events:
        if key_events.pressed:
            state["pressed_keys"].add(key_events.key_number)
        elif key_events.released:
            state["pressed_keys"].remove(key_events.key_number)

    if state["mode_select"]:
        select_mode()
    else:
        modes[state["mode"]]["func"](key_events)

    # ENCODER LOGIC

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:
        state["mode_select"] = not state["mode_select"]

        if state["mode_select"]:
            mode_select_view()
        else:
            modes[state["mode"]]["view"]()
