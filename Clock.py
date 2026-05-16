import time

starting_time = time.time()
last_time = starting_time
ticks = 0
ticks_last_second = 0
ticks_per_second = 60

def get_time():
    global starting_time
    return time.ticks_ms()/1000

def get_time_millis():
    #print(time.ticks_ms())
    return time.ticks_ms()
    
def tick():
    global ticks, ticks_last_second, ticks_per_second, last_time
    ticks+=1
    ticks_last_second+=1
    now = time.time()
    delta_time = now - last_time
    
    if delta_time:
        ticks_per_second = ticks_last_second / delta_time
        ticks_last_second = 0
        last_time = now