from pimoroni import Button
import Events

A = 0
B = 1
C = 2
UP = 3
DOWN = 4
BOOT = 5

buttons = [Button(7, invert=False), Button(8, invert=False), Button(9, invert=False), Button(22, invert=False), Button(6, invert=False), Button(23, invert=True)]
press_actions = [[],[],[],[],[],[],]
release_actions = [[],[],[],[],[],[],]
pressed = [False,False,False,False,False,False]

def update_needed():
    global buttons, pressed
    for button in range(0, len(buttons)):
        if (buttons[button].is_pressed and not pressed[button]) or (pressed[button] and not buttons[button].is_pressed):
            return True
    return False

def call_actions():
    result = False
    for button in range(0, len(buttons)):
        if buttons[button].is_pressed  and not pressed[button]:
            pressed[button] = True
            for action in press_actions[button]:
                action()
            result = True
        elif pressed[button] and not buttons[button].is_pressed:
            pressed[button] = False
            for action in release_actions[button]:
                action()
    return result

def on_press(button, funct):
    press_actions[button].append(funct)
    print(press_actions)
    
def on_release(button, funct):
    release_actions[button].append(funct)
    print(release_actions)
    
def rem_on_press(button, funct):
    if funct in press_actions[button]:
        press_actions[button].remove(funct)
    
def rem_on_release(button, funct):
    if funct in release_actions[button]:
        release_actions[button].remove(funct)
    
button_event = (call_actions, -2)

def Init():
    Events.add_pre_ui_event(button_event)