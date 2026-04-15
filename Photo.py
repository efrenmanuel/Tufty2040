from machine import ADC, Pin

lux = ADC(26)
_pin27 = None

def _get_pin27():
    global _pin27
    if _pin27 is None:
        _pin27 = Pin(27, Pin.OUT)
    return _pin27

def level():
    pin = _get_pin27()
    pin.value(1)
    val = lux.read_u16()
    pin.value(0)
    return val
