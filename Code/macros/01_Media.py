from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

app = {  # REQUIRED dict, must be named 'app'
    "name": "Media",  # Application name
    "macros": [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # top row
        (0x000000, "", [Keycode.CONTROL, Keycode.SHIFT, 'M']),
        (0x000000, "", [Keycode.LEFT_SHIFT,Keycode.LEFT_ARROW]),
        (0x000000, "", [Keycode.LEFT_SHIFT,Keycode.RIGHT_ARROW]),
        # middle row
        (0x000000, "", [Keycode.LEFT_SHIFT,Keycode.COMMA]),
        (0x000000, "", [Keycode.LEFT_SHIFT,Keycode.PERIOD]),
        (0x000000, "", [Keycode.LEFT_ARROW]),
        (0x000000, "", [Keycode.RIGHT_ARROW]),
        # bottom row
        (0x000000, "", [Keycode.SPACE,-Keycode.SPACE,Keycode.SPACE,-Keycode.SPACE]),
        (0x000000, "", [Keycode.GUI,Keycode.R,-Keycode.GUI,-Keycode.R,"""powershell\n""",0.1,"""$Audio = Get-AudioDevice -playback
if ($Audio.Name.StartsWith("DELL S2722DC")) {
   (Get-AudioDevice -list | Where-Object Name -like ("Speakers (Realtek(R) Audio)*") | Set-AudioDevice)
}  Else {
   (Get-AudioDevice -list | Where-Object Name -like ("DELL S2722DC*") | Set-AudioDevice)
}
exit\n"""]),
        (0x000000, "", [Keycode.LEFT_CONTROL,Keycode.LEFT_ARROW]),
        (0x000000, "", [Keycode.LEFT_CONTROL,Keycode.RIGHT_ARROW]),
        # Encoder buttons left encoder then right encoder 
        (0x000000, "", [[ConsumerControlCode.MUTE]]), # left encoder 
        (0x000000, "", [[ConsumerControlCode.PLAY_PAUSE]]), # right encoder 
    ],
    "encoders" : [
        (0x000000, "", [[ConsumerControlCode.VOLUME_DECREMENT]]), # left encoder, turn left 
        (0x000000, "", [[ConsumerControlCode.VOLUME_INCREMENT]]), # left encoder, turn right 
        (0x000000, "", [[ConsumerControlCode.VOLUME_DECREMENT]*2]), # right encoder, turn left 
        (0x000000, "", [[ConsumerControlCode.VOLUME_INCREMENT]*2]), # right encoder, turn right 
    ]
}
