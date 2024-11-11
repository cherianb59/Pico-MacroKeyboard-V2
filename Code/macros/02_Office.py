from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

app = {  # REQUIRED dict, must be named 'app'
    "name": "Office",  # Application name
    "macros": [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # top row
        (0x000000, "Music", [Keycode.CONTROL, Keycode.SHIFT, 'M']),
        (0x000000, "", [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x000000, "", [[ConsumerControlCode.PLAY_PAUSE]]),
        # middle row
        (0x000000, "Volume", [[ConsumerControlCode.MUTE]]),
        (0x000000, "", [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x000000, "", [[ConsumerControlCode.VOLUME_INCREMENT]]),
        (0x000000, "", [Keycode.GUI]),
        # bottom row
        (0x000000, "Discord", [Keycode.F13]),
        (0x000000, "", [Keycode.F14]),
        (0x000000, "", [Keycode.F15]),
        (0x000000, "", [Keycode.F16]),
        # Encoder buttons left encoder then right encoder 
        (0x000000, "MUTE", [{"buttons": Mouse.LEFT_BUTTON}]), # left encoder 
        (0x000000, "MUTE", [{"buttons": Mouse.LEFT_BUTTON}]), # right encoder 
    ],
    "encoders" : [
        (0x000000, "", [{"x":-1}]), # left encoder, turn left 
        (0x000000, "", [{"x": 1}]), # left encoder, turn right 
        (0x000000, "", [{"y":-1}]), # right encoder, turn left 
        (0x000000, "", [{"y": 1}]), # right encoder, turn right 
    ]
}
