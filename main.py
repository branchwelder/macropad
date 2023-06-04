from adafruit_macropad import MacroPad
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

macropad = MacroPad()

state = {
    "last_position": 0,
    "mode": 0,
    "mode_select": False,
    "brightness": 0.1,
    "color": {
        "h": 0.93,
        "s": 1,
        "v": 0.2
    },
    "color_mode": "solid",
    "offset": 0,
    "speed": 20,
    "pressed_keys": set()
}

scalar = float  # a scale value (0.0 to 1.0)


def hsv_to_rgb(h: scalar, s: scalar, v: scalar) -> tuple:
    if s:
        if h == 1.0:
            h = 0.0
        i = int(h*6.0)
        f = h*6.0 - i

        w = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        if i == 0:
            return (v*255, t*255, w*255)
        if i == 1:
            return (q*255, v*255, w*255)
        if i == 2:
            return (w*255, v*255, t*255)
        if i == 3:
            return (w*255, q*255, v*255)
        if i == 4:
            return (t*255, w*255, v*255)
        if i == 5:
            return (v*255, w*255, q*255)
    else:
        return (v*255, v*255, v*255)

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
    text_lines = macropad.display_text(title="HSV Crap")

    text_lines[0].text = "H {} - S {} - V{}".format(
        state["color"]["h"], state["color"]["s"], state["color"]["v"])
    text_lines[1].text = "Brightness {}".format(state["brightness"])
    text_lines[2].text = "Mode: {}".format(state["color_mode"])
    text_lines.show()


color_mode_map = {
    6: "solid",
    7: "cycle"
}


def rgb(key_events):
    encoder_pos = macropad.encoder

    if macropad.encoder > state["last_position"]:
        state["last_position"] = encoder_pos
        if 0 in state["pressed_keys"]:
            state["color"]["h"] = round((state["color"]["h"] + 0.01) % 1, 2)
        if 1 in state["pressed_keys"]:
            state["color"]["s"] = round((state["color"]["s"] + 0.1) % 1, 1)
        if 2 in state["pressed_keys"]:
            state["color"]["v"] = round((state["color"]["v"] + 0.1) % 1, 1)
        if 3 in state["pressed_keys"]:
            state["brightness"] = round((state["brightness"] + 0.02) % 1, 2)
        rgb_view()

    if macropad.encoder < state["last_position"]:
        if 0 in state["pressed_keys"]:
            state["color"]["h"] = round((state["color"]["h"] - 0.01) % 1, 2)
        if 1 in state["pressed_keys"]:
            state["color"]["s"] = round((state["color"]["s"] - 0.1) % 1, 1)
        if 2 in state["pressed_keys"]:
            state["color"]["v"] = round((state["color"]["v"] - 0.1) % 1, 1)
        if 3 in state["pressed_keys"]:
            state["brightness"] = round((state["brightness"] - 0.02) % 1, 2)

        state["last_position"] = encoder_pos
        rgb_view()

    if key_events:
        if key_events.pressed:
            if key_events.key_number == 6:
                state["color_mode"] = "solid"
            if key_events.key_number == 7:
                state["color_mode"] = "cycle"
        rgb_view()
# MAIN LOOP


modes = [
    {"title": "HSV Crap", "func": rgb, "view": rgb_view},
    {"title": "Media Controls", "func": media_controls, "view": media_view},
    {"title": "Num Pad", "func": num_pad, "view": num_pad_view}
]


modes[state["mode"]]["view"]()

tick = 0

while True:
    if state["color_mode"] == "solid":
        macropad.pixels.brightness = state["brightness"]
        macropad.pixels.fill(
            hsv_to_rgb(state["color"]["h"],
                       state["color"]["s"], state["color"]["v"]))
    elif state["color_mode"] == "cycle":
        macropad.pixels.brightness = state["brightness"]
        macropad.pixels.fill(
            hsv_to_rgb((state["color"]["h"]+state["offset"]) % 1,
                       state["color"]["s"], state["color"]["v"]))

        if ticks_ms() - tick > state["speed"]:
            state["offset"] += 0.005
            tick = ticks_ms()

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
