import Clock
import Image
import Buttons
import Events

active = False

def slide_auto_increase():
    return Image.slide_show(Clock.get_time_millis())


show_slide_event = (Image.show_slide,1)

slide_delay_increase_event = (Image.increase_slide_time,3)
slide_delay_decrease_event = (Image.decrease_slide_time,3)
slide_delay_show = (Image.show_slide_delay,999)


def up_flip():
    Events.flip_timer_event(slide_delay_increase_event)
    Events.flip_ui_event(slide_delay_show)
    Image.invalidate_display()

def down_flip():
    Events.flip_timer_event(slide_delay_decrease_event)
    Events.flip_ui_event(slide_delay_show)
    Image.invalidate_display()
    

slide_event = (slide_auto_increase, 0)

flip_slide_event=lambda:Events.flip_timer_event(slide_event)

def Init():
    global active
    if active:
        return
    active = True

    Image.invalidate_display()
    Events.add_ui_event(show_slide_event)
    Buttons.on_press(Buttons.A ,Image.slide_increase)
    Buttons.on_press(Buttons.B ,flip_slide_event)
    Buttons.on_press(Buttons.UP ,up_flip)
    Buttons.on_release(Buttons.UP ,up_flip)
    Buttons.on_press(Buttons.DOWN ,down_flip)
    Buttons.on_release(Buttons.DOWN ,down_flip)
    Buttons.on_press(Buttons.BOOT, Close)


def Close():
    global active
    if not active:
        return
    active = False

    Events.rem_timer_event(slide_event)
    Events.rem_timer_event(slide_delay_increase_event)
    Events.rem_timer_event(slide_delay_decrease_event)
    Events.remove_ui_event(show_slide_event)
    Events.remove_ui_event(slide_delay_show)
    Buttons.rem_on_press(Buttons.A ,Image.slide_increase)
    Buttons.rem_on_press(Buttons.B ,flip_slide_event)
    Buttons.rem_on_press(Buttons.UP ,up_flip)
    Buttons.rem_on_release(Buttons.UP ,up_flip)
    Buttons.rem_on_press(Buttons.DOWN ,down_flip)
    Buttons.rem_on_release(Buttons.DOWN ,down_flip)
    Buttons.rem_on_press(Buttons.BOOT, Close)

