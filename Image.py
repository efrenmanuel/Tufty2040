import Display
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
    slide_counter += 1
    if slide_counter == len(list_files):
        slide_counter = 0


def decrease_slide_time():
    global slide_time
    slide_time-=0.1
    if slide_time<=0:
        slide_time=0.1

def increase_slide_time():
    print("increase")
    global slide_time
    slide_time+=0.1


def slide_show(time):
    global last_slide_time
    #print(last_slide_time)
    print(slide_time*1000)
    #print(time)
    if (last_slide_time + slide_time*1000) < time:
        #print("increase")
        last_slide_time = time
        slide_increase()
        return True
    return False
    
def show_slide():
    #print(slide_counter)
    j.open_file(list_files[slide_counter])
    j.decode()
        
def show_image(image_name):
    #print(slide_counter)
    j.open_file(image_name+".jpg")
    j.decode()

        
def show_hidden_image(image_name):
    #print(slide_counter)
    j.open_file(image_name+".jpg_")
    j.decode()
    
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
