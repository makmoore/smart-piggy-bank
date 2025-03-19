# all libraries need to be imported to use
from rpi_lcd import LCD
import RPi.GPIO as GPIO
from time import sleep
import os.path


lcd = LCD() # initializes the lcd
lcd.clear() # clears any previous text on it
GPIO.setwarnings(False) # clears GPIO
GPIO.setmode(GPIO.BCM) # sets GPIO mode to receive from the raspi

# creating variable names for the GPIO pins used
dollar = 17
nickel = 22
dime = 23
quarter = 25
penny = 24

# sets up each pin and sets it to a LOW input
GPIO.setup(penny, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(nickel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dime, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(quarter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dollar, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:  # tries to read the total file if it exists already
    test = open("smart_bank_balance.txt", "r")  # reads file if it exists
    total = int(test.readline())  # saves teh value as the initial total balance
    test.close()  # closes the file
    lcd.text("Total: ${:0.2f}".format(total), 1) # displays on lcd
except:
    total = 0  # total balance begins at 0
    lcd.text("Total: ${:0.2f}".format(total), 1) # displays total on lcd

while True:
    if GPIO.input(penny) == True:
        total += 0.01
        lcd.text("Penny added!", 1)
        lcd.text("Total: {:0.2f}".format(total), 2)
        sleep(0.5)
    elif GPIO.input(nickel) == True:
        total += 0.05
        lcd.text("Nickel added!", 1)
        lcd.text("Total: {:0.2f}".format(total), 2)
        sleep(0.5)
    elif GPIO.input(dime) == True:
        total += 0.10
        lcd.text("Dime added!", 1)
        lcd.text("Total: {:0.2f}".format(total), 2)
        sleep(0.5)
    elif GPIO.input(quarter) == True:
        total += 0.25
        lcd.text("Quarter added!", 1)
        lcd.text("Total: {:0.2f}".format(total), 2)
        sleep(0.5)
    elif GPIO.input(dollar) == True:
        total += 1
        lcd.text("Dollar added!", 1)
        lcd.text("Total: {:0.2f}".format(total), 2)
        sleep(0.5)

    if KeyboardInterrupt():
        break

if os.path.exists("SmartPiggyBank/smart_bank_balance.txt"):  # if the file already exists, it deletes it
    os.remove("SmartPiggyBank/smart_bank_balance.txt")
save_amount = open("smart_bank_balance.txt", "w")  # creates and writes in the file
save_amount.write(str(total))  # writes the total in the file
save_amount.close() # closes file

GPIO.cleanup() # wipes GPIO board for next use