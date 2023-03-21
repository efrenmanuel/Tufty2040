# This example reads the voltage from a battery connected to Tufty 2040
# and uses this reading to calculate how much charge is left in the battery.
import Display
import Buttons
import Events
from machine import ADC, Pin

display=Display.display
display.set_backlight(0.8)

# set up the ADCs for measuring battery voltage
vbat_adc = ADC(29)
vref_adc = ADC(28)
vref_en = Pin(27)
vref_en.init(Pin.OUT)
vref_en.value(0)
usb_power = Pin(24, Pin.IN)         # reading GP24 tells us whether or not USB power is connected

# Reference voltages for a full/empty battery, in volts
# the values could vary by battery size/manufacturer so you might need to adjust them
# Values for a Galleon 400mAh LiPo:
full_battery = 3.7
empty_battery = 2.5

display.set_font("bitmap8")

width=35
height=15

top_left = (320-width-5,5)
nub_size = 8
nub_radius = 2

def show_battery():
    #print("inside show_battery")
    # The voltage reference on Tufty means we can measure battery voltage precisely, even when batteries are low.
    # Enable the onboard voltage reference
    vref_en.value(1)

    # Calculate the logic supply voltage, as will be lower that the usual 3.3V when running off low batteries
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = (
        (vbat_adc.read_u16() / 65535) * 3 * vdd
    )  # 3 in this is a gain, not rounding of 3.3V

    # Disable the onboard voltage reference
    vref_en.value(0)

    # Print out the voltage
    #print("Battery Voltage = ", vbat, "V", sep="")

    # convert the raw ADC read into a voltage, and then a percentage
    percentage = 100 * ((vbat - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100
    if percentage < 0:
        percentage = 0

    # draw the battery outline
    
    Display.set_color(Display.GREY)
    Display.rounded_rectangle(top_left[0],top_left[1],width-nub_size//2,height,2)
    Display.rounded_rectangle(top_left[0]+width-(nub_size//2)-nub_radius,top_left[1]+(height-nub_size)//2,nub_size//2 + nub_radius,nub_size, nub_radius)
    Display.set_color(Display.BLACK)
    Display.rounded_rectangle(top_left[0]+2,top_left[1]+2,width-4-nub_size//2,height-4,2)

    # draw a green box for the battery level
    Display.set_color(Display.GREEN)
    Display.rectangle(top_left[0]+2,top_left[1]+2, int(((width-4-nub_size//2) / 100) * percentage),height-4)

    # add text
    Display.set_color(Display.RED)
    if usb_power.value() == 1:         # if it's plugged into USB power...
        Display.text("USB", top_left[0]+4, top_left[1]+4, 240, 1)
    else:
        Display.text('{:.0f}%'.format(percentage), top_left[0]+4, top_left[1]+4, 240, 1)

#Display.update()

battery_event = (show_battery, 999)

def Init():
    Buttons.on_press(Buttons.C ,lambda:Events.add_ui_event(battery_event))
    Buttons.on_release(Buttons.C ,lambda:Events.remove_ui_event(battery_event))


def Close():
    Buttons.rem_on_press(Buttons.C ,lambda:Events.add_ui_event(battery_event))
    Buttons.rem_on_release(Buttons.C ,lambda:Events.remove_ui_event(battery_event))
