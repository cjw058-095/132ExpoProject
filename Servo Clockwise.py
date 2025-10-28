import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def unlock():
	print("Turning servo...")
	pwm.ChangeDutyCycle(6)
	time.sleep(0.123)
	pwm.ChangeDutyCycle(7.5)
	print("Locked in position.")

try:
	unlock()
finally:
	pwm.stop()
	GPIO.cleanup()
