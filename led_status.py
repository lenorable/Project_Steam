from machine import Pin

import time
import machine
import neopixel

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)

np = neopixel.NeoPixel(machine.Pin(13), 8)


def measure_distance():
    """
        Meet de afstand met de SR04
    """
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    while echo_pin.value() == 0:
        continue
    start = time.ticks_us()
    while echo_pin.value():
        continue
    end = time.ticks_us()

    diff = time.ticks_diff(end, start)

    distance = 0.034 * (diff/2)
    return distance


def led_status(distance):
    """
        Geeft door middel van de SR04
        de status aan op de WS2812
    """
    if distance <= 50:
        np[7] = [0, 255, 0]
        np[6] = [0, 0, 0]
        np.write()
        time.sleep_ms(1)
    if distance >= 50:
        np[7] = [0, 0, 0]
        np[6] = [255, 0, 0]
        np.write()
        time.sleep_ms(1)


while True:
    distance = measure_distance()
    led_status(distance)
    time.sleep_ms(1000)
