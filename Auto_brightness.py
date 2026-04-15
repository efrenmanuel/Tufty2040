import time
import Events
import Display
import Photo

last_display_brightness_update = 0
_initialized = False

def auto_brightness():
    global last_display_brightness_update, _initialized
    now = time.ticks_ms()
    if not _initialized or time.ticks_diff(now, last_display_brightness_update) > 500:
        _initialized = True
        lux = Photo.level()
        Display.auto_brightness(lux)
        last_display_brightness_update = now


auto_brightness_event = (auto_brightness, 0)

def Init():
    Events.add_timer_event_no_update(auto_brightness_event)
    
def End():
    Events.rem_timer_event_no_update(auto_brightness_event)