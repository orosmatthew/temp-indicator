import time
import board
import adafruit_dht
from gpiozero import AngularServo

servo = AngularServo(12, min_angle=-90, max_angle=90,
                     min_pulse_width=0.0005, max_pulse_width=0.0025)

dht_device = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9 / 5) + 32
        humidity = dht_device.humidity
        print(f'Temp: {temp_f:.2f} Humidity: {humidity:.2f}')
        if temp_f > 75:
            temp_f = 75
        if temp_f < 70:
            temp_f = 70
        angle = (((temp_f - 70) * 180) / 5 - 90) * -1
        if angle > 90:
            angle = 90
        if angle < -90:
            angle = -90
        print(f'Angle: {angle:.2f}')
        servo.angle = angle
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    time.sleep(2.0)



