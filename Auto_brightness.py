import Clock
import Events
import Display
import Photo

last_display_brightness_update = -3

def auto_brightness():
    global last_display_brightness_update
    if Clock.get_time_millis()-last_display_brightness_update > 500:
        Display.auto_brightness(Photo.level())
        print(Photo.level())
        last_display_brightness_update = Clock.get_time_millis()


auto_brightness_event = (auto_brightness, 0)

def Init():
    Events.add_timer_event_no_update(auto_brightness_event)
    
def End():
    Events.rem_timer_event_no_update(auto_brightness_event)