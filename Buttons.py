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
_num_buttons = len(buttons)
_deferred_ops = []
_in_callback = False

def _flush_deferred():
    global _deferred_ops
    ops = _deferred_ops
    _deferred_ops = []
    for op, args in ops:
        op(*args)

def call_actions():
    global _in_callback
    result = False
    _in_callback = True
    for button in range(_num_buttons):
        is_pressed = buttons[button].is_pressed
        if is_pressed and not pressed[button]:
            pressed[button] = True
            for action in list(press_actions[button]):
                action()
            result = True
        elif pressed[button] and not is_pressed:
            pressed[button] = False
            for action in list(release_actions[button]):
                action()
            result = True
    _in_callback = False
    if _deferred_ops:
        _flush_deferred()
    return result

def on_press(button, funct):
    if _in_callback:
        _deferred_ops.append((_do_on_press, (button, funct)))
        return
    _do_on_press(button, funct)

def _do_on_press(button, funct):
    if funct not in press_actions[button]:
        press_actions[button].append(funct)
    
def on_release(button, funct):
    if _in_callback:
        _deferred_ops.append((_do_on_release, (button, funct)))
        return
    _do_on_release(button, funct)

def _do_on_release(button, funct):
    if funct not in release_actions[button]:
        release_actions[button].append(funct)
    
def rem_on_press(button, funct):
    if _in_callback:
        _deferred_ops.append((_do_rem_on_press, (button, funct)))
        return
    _do_rem_on_press(button, funct)

def _do_rem_on_press(button, funct):
    if funct in press_actions[button]:
        press_actions[button].remove(funct)
    
def rem_on_release(button, funct):
    if _in_callback:
        _deferred_ops.append((_do_rem_on_release, (button, funct)))
        return
    _do_rem_on_release(button, funct)

def _do_rem_on_release(button, funct):
    if funct in release_actions[button]:
        release_actions[button].remove(funct)
    
button_event = (call_actions, -2)

def Init():
    Events.add_timer_event_no_update(button_event)