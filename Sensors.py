from machine import ADC, Pin

lux = ADC(26)
vbat_adc = ADC(Pin(29))   
vref_adc = ADC(Pin(28))

vref_en = Pin(27)
vref_en.init(Pin.OUT)
vref_en.value(0)

usb_power = Pin(24, Pin.IN)         # reading GP24 tells us whether or not USB power is connected

def lux_level():
    vref_en.value(1)
    val = lux.read_u16()
    vref_en.value(0)
    return val

def batt_level():
    vref_en.value(1)
    # Calculate the logic supply voltage, as will be lower that the usual 3.3V when running off low batteries
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = (
        (vbat_adc.read_u16() / 65535) * 3 * vdd
    )  # 3 in this is a gain, not rounding of 3.3V
    vref_en.value(0)
    return vbat

def usb_connected():
    return usb_power.value()
