import time
import board
import RPi.GPIO as GPIO
import pigpio

servo = 12
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)

temps = [70, 71, 72, 73, 74, 75]
temps_index = 0

while True:
    try:
        temp_f = temps[temps_index]
        humidity = 50.0
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
        if servo_pwm < 600: # should be 500
            servo_pwm = 600
        print(f'PWM: {servo_pwm:.2f}')
        pwm.set_servo_pulsewidth(servo, servo_pwm)
    except KeyboardInterrupt:
        pwm.set_PWM_dutycycle( servo, 0 )
        pwm.set_PWM_frequency( servo, 0 )

    temps_index += 1
    if temps_index > 5:
        temps_index = 0
    time.sleep(2.0)
