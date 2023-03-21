import Display
import Image
import Slides
import Events
import Buttons
import Battery


def start_slides():
    Slides.Init()
    print("slides")
    Close()

options=[("a) Images", start_slides),("b)",lambda:None), ("c)",lambda:None)]

selected = 0
def show_menu_bg():
    Image.show_hidden_image("menu_bg")

show_menu_bg_event = (show_menu_bg,1)

def show_options():
    line = 0
    for option in range(0,len(options)):
        if option == selected:
            Display.set_color(Display.WHITE)
        else:
            Display.set_color(Display.BLUE)
        Display.rounded_rectangle(10, 10+38*line, 200,28,3)
        if option == selected:
            Display.set_color(Display.BLUE)
        else:
            Display.set_color(Display.WHITE)
        Display.text(options[option][0], 15, 13+38*line, 240, 3)
        line+=1

show_options_event = (show_options,999)

def select():
    options[selected][1]()

def down():
    global selected
    selected+=1
    selected = selected % len(options)
    
def up():
    global selected
    selected-=1
    selected = selected % len(options)
    

def Init():
    Buttons.rem_on_release(Buttons.BOOT, Init)
    Events.add_ui_event(show_menu_bg_event)
    Events.add_ui_event(show_options_event)
    Buttons.on_press(Buttons.A, start_slides)
    Buttons.on_press(Buttons.UP, up)
    Buttons.on_press(Buttons.DOWN, down)
    Buttons.on_press(Buttons.B , select)

def Close():
    Buttons.on_release(Buttons.BOOT, Init)
    Events.remove_ui_event(show_menu_bg_event)  
    Events.remove_ui_event(show_options_event)
    Buttons.rem_on_press(Buttons.A ,start_slides)
    Buttons.rem_on_press(Buttons.UP, up)
    Buttons.rem_on_press(Buttons.DOWN, down)
    Buttons.rem_on_press(Buttons.B , select)
    #Buttons.rem_on_press(Buttons.B ,lambda:Events.flip_timer_event(slide_event))



def test():
    Slides.Init()