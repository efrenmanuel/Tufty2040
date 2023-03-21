import time

starting_time = time.time()
last_time = starting_time
ticks = 0
ticks_last_second = 0
ticks_per_second = 100

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
    delta_time = time.time() - last_time
    
    if delta_time:
        ticks_per_second = ticks_last_second*1.0/delta_time
        ticks_last_second = 0
        last_time = time.time()