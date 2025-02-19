import board, busio, displayio, os, terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import usb_hid
import digitalio
import time
import rotaryio
import keypad 
 
from adafruit_debouncer import Debouncer,Button

from adafruit_hid.mouse import Mouse

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from rainbowio import colorwheel
import neopixel


#________________________Neopixel____________________________________________________

pixel_pin = board.GP23
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

def color_chase(color):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()


def rainbow_cycle():
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        
       

# Set up Consumer Control - Control Codes can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html#ConsumerControlCode
consumer_control = ConsumerControl(usb_hid.devices)

# Set up a keyboard device. - Keycode can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html#Keycode
keyboard = Keyboard(usb_hid.devices)

mouse = Mouse(usb_hid.devices)

# Set up keyboard to write strings from macro
keyboard_layout = KeyboardLayoutUS(keyboard)

displayio.release_displays()

sda, scl = board.GP16, board.GP17  
try:
    i2c = busio.I2C(scl, sda)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    # Make the display context

    splash = displayio.Group()
    display.root_group = splash

    def draw_rectangle(splash):
    #clear screen and draw rectange 

        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(118, 54, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
        
        splash.append(inner_sprite)

except:
    splash = []
    def draw_rectangle(splash):
        pass 
        
draw_rectangle(splash)

splash.append(label.Label(terminalio.FONT, text = " Amazing"     , color=0xFFFF00, x=35, y=28))
splash.append(label.Label(terminalio.FONT, text = "MacroKeyboard", color=0xFFFF00, x=26, y=40))


#___________________Setup Keys____________________________

# These are the corresponding GPIOs on the Pi Pico that is used for the Keys on the PCB

pins = [board.GP0,board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP7,board.GP8,board.GP9,board.GP10,board.GP14,board.GP15,board.GP21]


keys = keypad.Keys(pins, value_when_pressed=True, pull=True)

#___________________Setup Rotary Encoder____________________________

encoder_1 = rotaryio.IncrementalEncoder(board.GP12, board.GP13)
encoder_2 = rotaryio.IncrementalEncoder(board.GP19, board.GP20)

#initial values for rotary encoders
encoder_1_last_position = -encoder_1.position
encoder_2_last_position = -encoder_2.position 


#___________________Setup Different Modes____________________________
# Load all the macro key setups from .py files in MACRO_FOLDER

MACRO_FOLDER = "/macros"
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()

for filename in files:
    if filename.endswith(".py"):
        try:
            module = __import__(MACRO_FOLDER + "/" + filename[:-3])
            apps.append(module.app)
        except (SyntaxError,ImportError,AttributeError,KeyError,NameError,IndexError,TypeError,) as err:
            print(err)
            pass

if not apps:
    draw_rectangle(splash)
    splash.append(label.Label(terminalio.FONT, text = "NO MACRO FILES", color=0xFFFF00, x=20, y=28))
    splash.append(label.Label(terminalio.FONT, text = "    FOUND"     , color=0xFFFF00, x = 20, y = 40))

    while True:
        pass

app_index = 0
apps[app_index]
apps_len = len(apps) 

time.sleep(1)
draw_rectangle(splash)            
splash.append(label.Label(terminalio.FONT, text = apps[app_index]['name'], color=0xFFFF00, x=20, y=28))
                
def execute_sequence(sequence):
# 'sequence' is an arbitrary-length list, each item is one of:
# Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
# Negative integer: (absolute value) key released
# Float (e.g. 0.25): delay in seconds
# String (e.g. "Foo"): corresponding keys pressed & released
# List []: one or more Consumer Control codes (can also do float delay)
# Dict {}: mouse buttons/motion (might extend in future)

    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                keyboard.press(item)
            else:
                keyboard.release(-item)
        elif isinstance(item, float):
            time.sleep(item)
        elif isinstance(item, str):    
            keyboard_layout.write(item,delay=None)
        elif isinstance(item, list):
            for code in item:
                if isinstance(code, int):
                    consumer_control.release()
                    consumer_control.press(code)
                if isinstance(code, float):
                    time.sleep(code)
        elif isinstance(item, dict):
            if "buttons" in item:
                if item["buttons"] >= 0:
                    mouse.press(item["buttons"])
                    print("press",item["buttons"])
                else:
                    mouse.release(-item["buttons"])
                    print("release",item["buttons"])
            mouse.move(
                item["x"] if "x" in item else 0,
                item["y"] if "y" in item else 0,
                item["wheel"] if "wheel" in item else 0,
            )

def release_sequence(sequence):
# Release any still-pressed keys, consumer codes, mouse buttons
# Keys and mouse buttons are individually released this way (rather
# than release_all()) because pad supports multi-key rollover, e.g.
# could have a meta key or right-mouse held down by one macro and
# press/release keys/buttons with others. Navigate popups, etc.
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                keyboard.release(item)
        elif isinstance(item, dict):
            if "buttons" in item:
                if item["buttons"] >= 0:
                    mouse.release(item["buttons"])
                    print("release",item["buttons"])
    consumer_control.release()
    
jiggle_time = time.monotonic()     
    
while True:
    first_time = time.monotonic()

    if (first_time - jiggle_time) > 120 :    
        mouse.move (x=1)
        time.sleep(0.001)
        mouse.move(x=-1)    
        jiggle_time = first_time

    #handle all encoder events before key presses 
        
    #print(encoder_1_last_position , -encoder_1.position)
    if   -encoder_1.position < encoder_1_last_position : 
        execute_sequence(apps[app_index]['encoders'][0][2])
        release_sequence(apps[app_index]['encoders'][0][2])
    elif -encoder_1.position > encoder_1_last_position : 
        execute_sequence(apps[app_index]['encoders'][1][2])
        release_sequence(apps[app_index]['encoders'][1][2])
    elif -encoder_2.position < encoder_2_last_position : 
        execute_sequence(apps[app_index]['encoders'][2][2])
        release_sequence(apps[app_index]['encoders'][2][2])
    elif -encoder_2.position > encoder_2_last_position : 
        execute_sequence(apps[app_index]['encoders'][3][2])
        release_sequence(apps[app_index]['encoders'][3][2])
    
    encoder_1_last_position = -encoder_1.position
    encoder_2_last_position = -encoder_2.position
    
    #now handle keypad events
    event = keys.events.get()
    
    if not event :
        continue  # No key events, or no corresponding macro, resume loop
    
    key_number = event.key_number
    pressed = event.pressed    
    print(key_number)
    if key_number == 13 : 
    # mode switch
        if pressed : 
            app_index = (app_index + 1) % apps_len
            draw_rectangle(splash)            
            splash.append(label.Label(terminalio.FONT, text = apps[app_index]['name'], color=0xFFFF00, x=20, y=28))
            
            keyboard.release_all()
            consumer_control.release()
            mouse.release_all()
            continue 
    else : 
    #normal keys
        sequence = apps[app_index]['macros'][key_number][2]

        if key_number not in (11,12):
            if pressed : execute_sequence(sequence)                               
            else: release_sequence(sequence) 
        else:
        #reverse for encoder buttons
            if pressed : release_sequence(sequence)                               
            else: execute_sequence(sequence) 
