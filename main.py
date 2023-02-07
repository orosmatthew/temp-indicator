import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import pigpio
from gpiozero import Buzzer
from configparser import ConfigParser

parser = ConfigParser()
parser.read("temp.conf")
temp_interval_seconds = float(parser.get("main", "temp_interval_seconds"))

dht_device = adafruit_dht.DHT11(board.D4)
servo = 12
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)

buzz = Buzzer(17)

while True:
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9 / 5) + 32
        humidity = dht_device.humidity
        buzz.on()
        time.sleep(0.02)
        buzz.off()
        print(f'Temp: {temp_f:.2f} Humidity: {humidity:.2f}')
        if temp_f > 75:
            temp_f = 75
        if temp_f < 70:
            temp_f = 70
        angle = (((temp_f - 70) * 180) / 5)
        if angle > 180:
            angle = 180
        if angle < 0:
            angle = 0
        print(f'Angle: {angle:.2f}')
        # 500 - 0 deg
        # 2500 - 180 deg
        servo_pwm = (2000 - (angle * 2000) / 180) + 500
        if servo_pwm > 2500:
            servo_pwm = 2500
        if servo_pwm < 600:  # should be 500, but 600 seems to work better
            servo_pwm = 600
        print(f'PWM: {servo_pwm:.2f}')
        pwm.set_servo_pulsewidth(servo, servo_pwm)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    except KeyboardInterrupt:
        pwm.set_PWM_dutycycle(servo, 0)
        pwm.set_PWM_frequency(servo, 0)
    time.sleep(temp_interval_seconds)
