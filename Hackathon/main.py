# EERSTE DOEN ONS DIE IMPORTS
import time
import board
import digitalio
import analogio
from time import sleep
import usb_hid
import pwmio
import neopixel
import random
from functions import *


# DAN DECLARE ONS ALLES
# button
btn1 = digitalio.DigitalInOut(board.GP15)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP
# button_state = True

# Joystick
x_axis = analogio.AnalogIn(board.GP26)
y_axis = analogio.AnalogIn(board.GP27)

joyBTN = digitalio.DigitalInOut(board.GP18)
joyBTN.direction = digitalio.Direction.INPUT
joyBTN.pull = digitalio.Pull.UP

# LED ring
num_pixels = 60
pixels = neopixel.NeoPixel(board.GP19, num_pixels)
pixels.brightness = 0.5

# Buzzer
buzzer = digitalio.DigitalInOut(board.GP0)
buzzer.direction = digitalio.Direction.OUTPUT

# Spedometer
# Define spedo pins
sped1 = digitalio.DigitalInOut(board.GP1)
sped1.direction = digitalio.Direction.OUTPUT

sped2 = digitalio.DigitalInOut(board.GP2)
sped2.direction = digitalio.Direction.OUTPUT

sped3 = digitalio.DigitalInOut(board.GP3)
sped3.direction = digitalio.Direction.OUTPUT

sped4 = digitalio.DigitalInOut(board.GP4)
sped4.direction = digitalio.Direction.OUTPUT

sped5 = digitalio.DigitalInOut(board.GP5)
sped5.direction = digitalio.Direction.OUTPUT

sped6 = digitalio.DigitalInOut(board.GP6)
sped6.direction = digitalio.Direction.OUTPUT

sped7 = digitalio.DigitalInOut(board.GP7)
sped7.direction = digitalio.Direction.OUTPUT

sped8 = digitalio.DigitalInOut(board.GP8)
sped8.direction = digitalio.Direction.OUTPUT

def set_led_brightness(index, brightness):
    r, g, b = pixels[index]
    pixels[index] = (255, 0, 0)


# Function to generate a random egg position
def generate_egg_position():
    return random.randint(0, 59)


while True:

    while joyBTN.value:

        pass
    
    dragon_position = 30
    egg_position = generate_egg_position()
    score = 0
    round_timer = 0
    speed = 1
    length = -2

    try:
        while True:
            # Map the joystick values to LED index (0 to 59)
            # led_index = int(interval_mapping(x_axis.value, 0, 65535, 0, 60))
            joyValX = int(interval_mapping(x_axis.value, 0, 65535, 0, 10000))
            # print("joyValX", joyValX)

            round_start_time = time.monotonic()

            if joyValX >= 5000:
                led_index =  +speed
            elif joyValX <= 2500:
                led_index =  -speed
            else:
                led_index = 0
                
            # print("LEdIndes", led_index)

            # Turn off all LEDs
            pixels.fill((0, 0, 0))

            # Turn on the dragon and its neighbors
            for i in range(length, 3):
                index = (dragon_position + i) % 60
                # brightness = 0.5 # Dim the LEDs farther from the center
                brightness = 1.0 - (abs(i) * 0.2)  # Dim the LEDs farther from the center
                set_led_brightness(index, brightness)

            # Update the dragon position and wrap around the ring
            dragon_position = (dragon_position + led_index)
            if (dragon_position >= 61):
                dragon_position = dragon_position -60
            if (dragon_position <= -1):
                dragon_position = dragon_position + 60

            # Turn on the egg
            pixels[egg_position] = (0, 255, 0)  # Set the egg color (green)

            # Check if any of the 5 LEDs of the dragon are on the egg and the button is pressed
            if dragon_position in range(egg_position - 2, egg_position + 3):
                if not btn1.value:
                    # Pick up the egg and generate a new egg position
                    egg_position = generate_egg_position()
                    # Increase the player's score by 1
                    score += 1
                    # resets round timer
                    round_timer = 0
                    # Plays a buzzer jingle
                    buzzer.value = True
                    time.sleep(0.5)
                    buzzer.value = False
            if dragon_position not in range(egg_position - 2, egg_position + 3):
                if not btn1.value:
                    print("Missed!", dragon_position in range(egg_position - 2, egg_position + 3))
                    # Plays a buzzer jingle
                    buzzer.value = True
                    time.sleep(0.5)
                    buzzer.value = False
                    break

            # calculates time
            round_timer = time.monotonic() - round_start_time

            # calculates score
            if score >= 1:
                sped1.value = True

            if score >= 2:
                sped2.value = True

            if score >= 3:
                sped3.value = True

            if score >= 4:
                speed = 2
                sped4.value = True

            if score >= 5:
                sped5.value = True

            if score >= 6:
                sped6.value = True

            if score >= 7:
                sped7.value = True
                length = -1

            if score >= 8:
                sped8.value = True
                speed = 3
                length = 0
            
            if score == 9:
                break

            # Check if the round timer has exceeded 10 seconds
            if round_timer >= 10:
                break


            # Add a small delay to avoid flickering
            # print("egg pos: " , egg_position)
            # print("Dragon pos: " , dragon_position)
            # print(btn1.value)
            # print("x axis: " + str(round(interval_mapping(x_axis.value, 0, 65535, 0, 60))), 1)
            print("Score: " + str(score))

        if score == 9:
            pixels.fill((0, 255, 0))
            buzzer.value = True
            time.sleep(1)
            pixels.fill((0, 0, 0))
            buzzer.value = False
            time.sleep(1)
            pixels.fill((0, 255, 0))
            buzzer.value = True
            time.sleep(1)
            pixels.fill((0, 0, 0))
            buzzer.value = False
            time.sleep(1)
            pixels.fill((0, 255, 0))
            buzzer.value = True
            time.sleep(1)
            pixels.fill((0, 0, 0))
            buzzer.value = False
            time.sleep(1)
            sped1.value = False
            sped2.value = False
            sped3.value = False
            sped4.value = False
            sped5.value = False
            sped6.value = False
            sped7.value = False
            sped8.value = False
        else:
            pixels.fill((255, 0, 0))
            buzzer.value = True
            time.sleep(1)
            pixels.fill((0, 0, 0))
            buzzer.value = False
            time.sleep(1)
            pixels.fill((255, 0, 0))
            buzzer.value = True
            time.sleep(1)
            pixels.fill((0, 0, 0))
            buzzer.value = False
            time.sleep(1)
            pixels.fill((255, 0, 0))
            buzzer.value = True
            time.sleep(1)
            pixels.fill((0, 0, 0))
            buzzer.value = False
            time.sleep(1)
            sped1.value = False
            sped2.value = False
            sped3.value = False
            sped4.value = False
            sped5.value = False
            sped6.value = False
            sped7.value = False
            sped8.value = False

            
            
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, exit gracefully
        pixels.fill((0, 0, 0))

    while not joyBTN.value:
        pass

    pixels.fill((0,0,0))