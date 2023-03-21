from machine import ADC, Pin
from time import sleep
lux_pwr = Pin(27, Pin.OUT)

lux = ADC(26)

def level():
    lux_pwr.value(1)
    val = lux.read_u16()
    
    lux_pwr.value(0)
    return val
