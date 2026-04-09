# Met la pin de reset des esp a 0
import RPi.GPIO as GPIO
rest_pin = 36

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rest_pin, GPIO.OUT)
    GPIO.output(rest_pin, GPIO.LOW)
    print("Pin de reset mise à LOW pour réinitialiser les ESPs.")
except Exception as e:
    print(f"Erreur lors de la configuration de la pin de reset: {e}")
finally:
    GPIO.cleanup()