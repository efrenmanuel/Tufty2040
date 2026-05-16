import Display
import Events
import os
import time
from jpegdec import JPEG

display = Display.display
j = JPEG(display)

def show_image():
    global j
    j.open_file("rainbow.jpg")
    j.decode()

slide_counter = 0
slide_time = 1
list_files=[]
last_slide_time = 0
_current_display_image = None
def load_image_list():
    for file in os.listdir(""):
    # check only image files
        if file.endswith('.jpg'):
            list_files.append(file)


def load_set_image_list():
    global list_files
    list_files=["1.jpg", "2.jpg"]

def slide_increase():
    global slide_counter
    if not list_files:
        return
    slide_counter += 1
    if slide_counter == len(list_files):
        slide_counter = 0
    invalidate_display()
    Events.request_ui_update()


def decrease_slide_time():
    global slide_time
    slide_time-=0.1
    if slide_time<=0:
        slide_time=0.1
    return True

def increase_slide_time():
    global slide_time
    slide_time+=0.1
    return True


def invalidate_display():
    global _current_display_image
    _current_display_image = None

def slide_show(now):
    global last_slide_time
    if time.ticks_diff(now, last_slide_time) > slide_time * 1000:
        last_slide_time = now
        slide_increase()
        return True
    return False
    
def show_slide():
    global _current_display_image
    if not list_files:
        return
    target = list_files[slide_counter]
    if _current_display_image != target:
        j.open_file(target)
        j.decode()
        _current_display_image = target
        
def show_image(image_name):
    global _current_display_image
    filename = image_name+".jpg"
    if _current_display_image != filename:
        j.open_file(filename)
        j.decode()
        _current_display_image = filename

        
def show_hidden_image(image_name):
    global _current_display_image
    filename = image_name+".jpg_"
    if _current_display_image != filename:
        j.open_file(filename)
        j.decode()
        _current_display_image = filename
    
def show_slide_delay():
    Display.set_color(Display.WHITE)
    Display.rectangle(10,207, 200,28)
    Display.set_color(Display.BLACK)
    Display.text('{:.2f} seconds'.format(slide_time), 15, 210, 240, 3)

load_image_list()

if __name__ == "__main__":
    while True:
        Display.clear()
        slide_show(time.time())
        show_image()
        show_slide_delay()
        Display.update()
