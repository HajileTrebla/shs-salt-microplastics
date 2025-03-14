import RPi.GPIO as GPIO

def loop():
    global btn
    print(GPIO.input(btn))


def main():
    global btn

    btn = 7

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        loop()

if __name__ == "__main__":
    main()