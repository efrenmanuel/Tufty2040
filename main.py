import time
import Clock
import Display
import Auto_brightness
import Battery
import Buttons
import Events
import Menu
import _thread
import machine

running = True
 
updates_per_second = 60
milliseconds_per_update = max(1, int(1000 / updates_per_second))

screen_refresh_rate = 60
milliseconds_per_refresh = max(1, int(1000 / screen_refresh_rate))


def Init():
    #Initialize every module we want to use
    Display.Init()
    Auto_brightness.Init()
    Buttons.Init()
    Battery.Init()
    Menu.Init()

Init()
#force first updates
Events.update_no_ui()
Events.update_ui()
Display.update()


def loop(events):
    next_refresh = time.ticks_ms()
    while running:
        events.run_queues()

        next_refresh = time.ticks_add(next_refresh, milliseconds_per_refresh)
        remaining = time.ticks_diff(next_refresh, time.ticks_ms())
        if remaining > 1:
            time.sleep_ms(remaining)
        else:
            next_refresh = time.ticks_ms()
            time.sleep_ms(1)

def bg_loop(events):
    global running
    next_update = time.ticks_ms()
    
    try:
        while running:
            events.run_bg_queues()
            Clock.tick()

            next_update = time.ticks_add(next_update, milliseconds_per_update)
            remaining = time.ticks_diff(next_update, time.ticks_ms())
            if remaining > 1:
                time.sleep_ms(remaining)
            else:
                next_update = time.ticks_ms()
                time.sleep_ms(1)
    except Exception:
        running = False
        
def stop():
    global running
    running=False

if __name__ == "__main__":
    Buttons.on_press(Buttons.BOOT, stop)
    try:
        BGThread = _thread.start_new_thread(bg_loop, (Events,))
        loop(Events) # doesn't return
    except KeyboardInterrupt:
        machine.reset()
    while True:
        time.sleep(10)
        
