import time
import Clock
#import Image
import Display
import Auto_brightness
import Battery
import Buttons
import Events
import Menu
#import Test3d

from pimoroni import Button

display = Display.display
 
updates_per_second = 100
seconds_per_update = 1/updates_per_second
last_update = Clock.get_time_millis()

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

while True:
    Events.run_queues(Buttons.update_needed())
    Clock.tick()

    time.sleep((last_update + seconds_per_update*1000 - Clock.get_time_millis())/1000)
    last_update = Clock.get_time_millis()


