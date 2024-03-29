import pandas as pd
import numpy as np
import os
import logging

from tabulate import tabulate

import colorama
from colorama import Fore

from threading import Timer
import time
from random import randrange

from neopixel import *
import RPi.GPIO as GPIO
import serial

dataset = None
preview_dataset = None

LED_COUNT = 256      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 40     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

WIN_LIMIT = 2
TRY_LIMIT = 4

GPIO.setmode(GPIO.BCM)


#
# PINS
##########
# eight_channel_relay_in  = [5, 20, 26, 19,  6, 12, 16, 21]
# eight_channel_relay_out = [4, 17, 27, 22, 23, 24, 25,  8]  # 13 use button like

eight_channel_relay_in = [5, 20, 26, 19,  6, 12, 16, 21]
eight_channel_relay_out = [4, 17, 27, 22, 23, 24, 25,  8]  # 13 use button like
FANPIN = 10  # 19
CONTROLLERPIN = 7  # 19


#
# SETUPS
##########
for i in eight_channel_relay_in:
    GPIO.setup(i, GPIO.OUT)
for i in eight_channel_relay_out:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(FANPIN, GPIO.OUT)
GPIO.output(FANPIN, GPIO.LOW)
# Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(CONTROLLERPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(CONTROLLERPIN, GPIO.RISING, bouncetime=1)
#
# INIT
##########
for i in eight_channel_relay_in:
    GPIO.output(i, GPIO.LOW)


def clear_screen(): return os.system('clear')


def prepare_datasets():
    global dataset, preview_dataset

    nrows, ncols = [], []
    pre_rows, pre_cols = [], []

    # Initalize table
    change = False
    for i in range(1, 257):
        led_max_count = i % 16

        if (led_max_count != 0):
            nrows.append(str(i-1))
            # pre_rows.append('.')
            pre_rows.append('')
        else:
            nrows.append(str(i-1))
            # pre_rows.append('.')
            pre_rows.append('')

            if(change):
                ncols.append(nrows[::-1])
                change = False
            else:
                ncols.append(nrows)
                change = True
            pre_cols.append(pre_rows)

            nrows = []
            pre_rows = []

    matrix_data = np.column_stack(ncols)
    dataset = pd.DataFrame({0: matrix_data[:, 0], 1: matrix_data[:, 1], 2: matrix_data[:, 2], 3: matrix_data[:, 3],
                            4: matrix_data[:, 4], 5: matrix_data[:, 5], 6: matrix_data[:, 6], 7: matrix_data[:, 7],
                            8: matrix_data[:, 8], 9: matrix_data[:, 9], 10: matrix_data[:, 10], 11: matrix_data[:, 11],
                            12: matrix_data[:, 12], 13: matrix_data[:, 13], 14: matrix_data[:, 14], 15: matrix_data[:, 15]})

    preview_data = np.column_stack(pre_cols)
    preview_dataset = pd.DataFrame({0: preview_data[:, 0], 1: preview_data[:, 1], 2: preview_data[:, 2], 3: preview_data[:, 3],
                                    4: preview_data[:, 4], 5: preview_data[:, 5], 6: preview_data[:, 6], 7: preview_data[:, 7],
                                    8: preview_data[:, 8], 9: preview_data[:, 9], 10: preview_data[:, 10], 11: preview_data[:, 11],
                                    12: preview_data[:, 12], 13: preview_data[:, 13], 14: preview_data[:, 14], 15: preview_data[:, 15]})

    return dataset, preview_dataset


def accdata(row, col, value='', preview=False):
    global dataset, preview_dataset
    if (value != '' and preview):
        # preview_dataset.iloc[row, col] = 'O'
        preview_dataset.iloc[row, col] = value

        return dataset.iloc[row, col], preview_dataset.iloc[row, col]

    if (preview):
        return dataset.iloc[row, col], preview_dataset.iloc[row, col]

    return int(dataset.iloc[row, col])


def shift_object(x=0, y=0, shiftobject=None):
    for obj in shiftobject:
        if(x != 0):
            obj[0] = obj[0] + x

        if(y != 0):
            obj[1] = obj[1] + y

    return shiftobject


def draw_frame(strip, color):
    # Rahmen
    clear_table(strip, Color(0, 0, 0), all=True)
    wait_ms = 50
    for i in range(16):
        # accdata(0, i, value='O', preview=True)
        strip.setPixelColor(accdata(0, i), color)
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(16):
        # accdata(i, 0, value='O', preview=True)
        strip.setPixelColor(accdata(i, 0), color)
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(16):
        # accdata(15, i, value='O', preview=True)
        strip.setPixelColor(accdata(15, i), color)
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(16):
        # accdata(i, 15, value='O', preview=True)
        strip.setPixelColor(accdata(i, 15), color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def getnumbers(number=None, size=0):
    '''
        Get numbers coordinates
        size = {0(small, two digit), 1(big, one digit) }    
    '''

    if (size == 0):
        zero = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [11, 0], [
            11, 1], [11, 2], [11, 3], [11, 4], [10, 4], [9, 4], [8, 4], [7, 4], [6, 4], [5, 4], [4, 4], [3, 4], [2, 4], [1, 4], [0, 4], [0, 3], [0, 2], [0, 1]]

        one = [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
               [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4]]

        two = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [6, 0], [
            6, 1], [6, 2], [6, 3], [6, 4], [7, 0], [8, 0], [9, 0], [10, 0], [11, 4], [11, 3], [11, 2], [11, 1], [11, 0]]

        three = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
                 [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [
                     11, 4], [11, 3], [11, 2], [11, 1], [11, 0],
                 [6, 3], [6, 2], [6, 1], [6, 0]]

        four = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [
                6, 0], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [
                6, 4], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [6, 1], [6, 2], [6, 3]]

        five = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [
            6, 1], [6, 2], [6, 3], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [11, 3], [11, 2], [11, 1], [11, 0]]

        six = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [
            9, 0], [10, 0], [11, 0], [11, 1], [11, 2], [11, 3], [11, 4], [10, 4], [9, 4], [8, 4], [7, 4], [6, 4], [6, 3], [6, 2], [6, 1]]

        seven = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
                 [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4]]

        eight = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
                 [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [
                     11, 4], [11, 3], [11, 2], [11, 1], [11, 0],
                 [6, 3], [6, 2], [6, 1], [6, 0], [0, 0], [
                     1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
                 [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0]]

        nine = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
                [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [
                    11, 4], [11, 3], [11, 2], [11, 1], [11, 0],
                [6, 3], [6, 2], [6, 1], [6, 0], [0, 0], [
                    1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
                [6, 0]]

    if (size == 1):
        zero = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [
            11, 1], [11, 2], [11, 3], [11, 4], [11, 5], [10, 5], [9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1]]

        one = [[0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
               [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5]]

        two = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [6, 0], [
            6, 1], [6, 2], [6, 3], [6, 4], [7, 0], [8, 0], [9, 0], [10, 0], [11, 5], [11, 4], [11, 3], [11, 2], [11, 1], [11, 0]]

        three = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [5, 5],
                 [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5], [
                     11, 4], [11, 3], [11, 2], [11, 1], [11, 0],
                 [6, 4], [6, 3], [6, 2], [6, 1], [6, 0]]

        four = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [
                6, 0], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [
                6, 5], [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5], [6, 1], [6, 2], [6, 3], [6, 4]]

        five = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [
            6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5], [11, 4], [11, 3], [11, 2], [11, 1], [11, 0]]

        six = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [
            9, 0], [10, 0], [11, 0], [11, 1], [11, 2], [11, 3], [11, 4], [11, 5], [10, 5], [9, 5], [8, 5], [7, 5], [6, 5], [6, 4], [6, 3], [6, 2], [6, 1]]

        seven = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
                 [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5]]

        eight = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
                 [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5], [
                     11, 4], [11, 3], [11, 2], [11, 1], [11, 0],
                 [6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [0, 0], [
                     1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
                 [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0]]

        nine = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
                [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5], [
                    11, 4], [11, 3], [11, 2], [11, 1], [11, 0],
                [6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [0, 0], [
                    1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
                [6, 0]]

    if (number == 0):
        return zero
    if (number == 1):
        return one
    if (number == 2):
        return two
    if (number == 3):
        return three
    if (number == 4):
        return four
    if (number == 5):
        return five
    if (number == 6):
        return six
    if (number == 7):
        return seven
    if (number == 8):
        return eight
    if (number == 9):
        return nine


def draw_number(number=None, strip=None, color=None):
    num = number
    num1 = None
    num2 = None
    wait_ms = 50

    if (len(str(number)) > 1):
        num1, num2 = str(number)
        num1 = int(num1)
        num2 = int(num2)

    if (num1 != None and num2 != None):
        num1 = shift_object(2, 2, getnumbers(num1, 0))
        num2 = shift_object(2, 9, getnumbers(num2, 0))

        for pixel in num1:
            # accdata(pixel[0], pixel[1], 'O', preview=True)
            strip.setPixelColor(accdata(pixel[0], pixel[1]), color)
            # strip.show()
            # time.sleep(wait_ms/2000.0)
            # print(pixel[0], pixel[1], accdata(pixel[0], pixel[1]))
            # print("Setting pixel:", accdata(pixel[0], pixel[1]))
        for pixel2 in num2:
            # accdata(pixel2[0], pixel2[1], 'O', preview=True)
            strip.setPixelColor(accdata(pixel2[0], pixel2[1]), color)
            # time.sleep(wait_ms/2000.0)

            # print(pixel2[0], pixel2[1], accdata(pixel2[0], pixel2[1]))
        strip.show()
    else:
        num = shift_object(2, 5, getnumbers(num, 1))
        for pixel in num:
            # accdata(pixel[0], pixel[1], 'O', preview=True)
            strip.setPixelColor(accdata(pixel[0], pixel[1]), color)
        strip.show()
        # time.sleep(wait_ms/2000.0)


def draw_lose_win(strip, color):
    clear_table(strip, Color(0, 0, 0))

    for x in range(0, 16):
        for y in range(0, 16):
            # accdata(x, y, " ", preview=True)
            strip.setPixelColor(accdata(x, y), color)
    strip.show()
    # time.sleep(wait_ms/2000.0)

    time.sleep(1)
    clear_table(strip, Color(0, 0, 0))
    time.sleep(1)

    for x in range(0, 16):
        for y in range(0, 16):
            # accdata(x, y, " ", preview=True)
            strip.setPixelColor(accdata(x, y), color)
    strip.show()
    # time.sleep(wait_ms/2000.0)

    time.sleep(1)
    clear_table(strip, Color(0, 0, 0))
    time.sleep(1)

    for x in range(0, 16):
        for y in range(0, 16):
            # accdata(x, y, " ", preview=True)
            strip.setPixelColor(accdata(x, y), color)
    strip.show()


def clear_table(strip, color, all=False):
    area_from = 1
    area_to = 15

    if all:
        area_from = 0
        area_to = 16

    for x in range(area_from, area_to):
        for y in range(area_from, area_to):
            # accdata(x, y, " ", preview=True)
            strip.setPixelColor(accdata(x, y), color)
    strip.show()


def draw_animate(strip, colors, serial):
    running = True

    tmplist = list(eight_channel_relay_out)
    win_list = []

    while len(win_list) < 4:
        rand_item = randrange(8)
        if (rand_item >= len(tmplist)):
            continue
        win_list.append(tmplist[rand_item])
        tmplist.pop(rand_item)

    seconds = 60
    win_counter = 0
    while running:
        plugged = []
        if(seconds == 60 or seconds == 20):
            serial.write(str.encode("c"))

        if (seconds == 0):
            serial.write(str.encode("q"))
            running = False

        clear_table(strip, Color(0, 0, 0))
        draw_number(number=seconds, strip=strip, color=colors)

        if(GPIO.input(eight_channel_relay_out[0])):
            if (eight_channel_relay_out[0] not in plugged):
                plugged.append(eight_channel_relay_out[0])
        if(GPIO.input(eight_channel_relay_out[1])):
            if (eight_channel_relay_out[1] not in plugged):
                plugged.append(eight_channel_relay_out[1])
        if(GPIO.input(eight_channel_relay_out[2])):
            if (eight_channel_relay_out[2] not in plugged):
                plugged.append(eight_channel_relay_out[2])
        if(GPIO.input(eight_channel_relay_out[3])):
            if (eight_channel_relay_out[3] not in plugged):
                plugged.append(eight_channel_relay_out[3])
        if(GPIO.input(eight_channel_relay_out[4])):
            if (eight_channel_relay_out[4] not in plugged):
                plugged.append(eight_channel_relay_out[4])
        if(GPIO.input(eight_channel_relay_out[5])):
            if (eight_channel_relay_out[5] not in plugged):
                plugged.append(eight_channel_relay_out[5])
        if(GPIO.input(eight_channel_relay_out[6])):
            if (eight_channel_relay_out[6] not in plugged):
                plugged.append(eight_channel_relay_out[6])
        if(GPIO.input(eight_channel_relay_out[7])):
            if (eight_channel_relay_out[7] not in plugged):
                plugged.append(eight_channel_relay_out[7])

        win_counter = 0
        for plug in plugged:
            for win in win_list:
                if (win_counter >= WIN_LIMIT):
                    logging.info("[*] GEWONNEN")
                    serial.write(str.encode("f"))
                    draw_lose_win(strip, Color(255, 0, 0))
                    GPIO.output(FANPIN, GPIO.LOW)
                    return
                elif(len(plugged)>=TRY_LIMIT and win_counter <= WIN_LIMIT):
                    logging.info("[*] VERLOREN **")
                    serial.write(str.encode("a"))
                    draw_lose_win(strip, Color(0, 255, 0))
                    return

                if (plug == win):
                    win_counter = win_counter + 1

        # time managing
        seconds = seconds - 1
        time.sleep(1)

    GPIO.output(FANPIN, GPIO.LOW)
    serial.write(str.encode("a"))
    draw_lose_win(strip, Color(0, 255, 0))
    logging.info("[*] VERLOREN *")


def main(serial, strip):
    try:
        GPIO.output(FANPIN, GPIO.HIGH)
        draw_frame(strip, Color(0, 255, 0))
        draw_animate(strip, Color(0, 255, 0), serial)
        GPIO.output(FANPIN, GPIO.LOW)

    except KeyboardInterrupt:
        clear_table(strip, Color(0, 0, 0), all=True)
        serial.write(str.encode("q"))
        GPIO.cleanup()


if __name__ == "__main__":
    # global dataset, preview_dataset
    print("[*] Init logger")
    logging.basicConfig(level=logging.INFO,filename='/home/pi/app.log', filemode='a', format='[ %(asctime)s ] %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    
    logging.info("[*] PROGRAMM STARTED")

    logging.info('[*] Open serial')
    serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(5)

    logging.info("[*] Preparing matrix for Led table")
    prepare_datasets()

    logging.info("[*] Init Neopixel")
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    draw_frame(strip, Color(0, 0, 255))

    logging.info("[*] Starting main")
    while True:
        time.sleep(0.25)
        if GPIO.event_detected(CONTROLLERPIN):
            GPIO.remove_event_detect(CONTROLLERPIN)
            main(serial, strip)
            time.sleep(1)
            GPIO.add_event_detect(CONTROLLERPIN, GPIO.RISING, bouncetime=1)

    # main()


# PRETTY PRINT DATASET
#        print(tabulate(preview_dataset, headers='keys',
#                       tablefmt='fancy_grid', stralign='center'))

# FULL DATASET
# print(dataset)

# draw_number(number1=9, number2=3)
# draw_number(number=9)

# PRETTY PRINT DATASET
# print(tabulate(preview_dataset, headers='keys',
#                tablefmt='fancy_grid', stralign='center'))
