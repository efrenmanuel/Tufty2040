import Events
from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = PicoGraphics(display=DISPLAY_TUFTY_2040)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(190, 190, 190)
TEAL = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
RED = display.create_pen(255, 0, 0)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)


brightness=.99
display.set_backlight(brightness) # has to be between .3 and .99

line = display.line
rectangle = display.rectangle
set_color = display.set_pen
text = display.text
update = display.update
get_bounds = display.get_bounds

def rounded_rectangle(x, y, w, h, radius):
    
    display.rectangle(x+radius, y, w-radius*2, h)
    display.rectangle(x, y+radius, w, h-radius*2)
    
    display.circle(x+radius, y+radius, radius)
    display.circle(x+w-radius-1, y+radius, radius)
    display.circle(x+radius, y+h-radius-1, radius)
    display.circle(x+w-radius-1, y+h-radius-1, radius)
    
def update_brightness(new_brightness):
    global brightness
    if new_brightness>=1:
        new_brightness=.99
    elif new_brightness<=.35:
        new_brightness=.37
    if (abs(new_brightness-brightness)>=0.05):
        brightness=new_brightness
        display.set_backlight(brightness) # has to be between .3 and .99
        print(brightness)

def clear(color=BLACK):
    display.set_pen(color)
    display.clear()
        
def auto_brightness(lux):
    new_brightness=((lux/50000)**.4)*.63+.32
    update_brightness(new_brightness)
        #print(last_display_brightness_update)

def Init():
    display_clear_event = (clear, -1)

    display_update_event = (update, 99999)

    Events.add_ui_event(display_clear_event)
    Events.add_ui_event(display_update_event)