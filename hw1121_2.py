#PWM LED 제어 - 버튼을 클릭하면 LED가 10단계로 밝아졌다가 꺼지기를 반복합니다.
import RPi.GPIO as GPIO
import time

LED=4
KEY = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT) 

try:
    pwm = GPIO.PWM(LED, 100)
    pwm.start(0)    
    while True:
        if GPIO.input(KEY)==True:
            for i in range(10):
                pwm.ChangeDutyCycle(i*10)
                time.sleep(1)    
        GPIO.output(LED,False)

except KeyboardInterrupt:
    pass
finally:
pwm.stop()
GPIO.cleanup()
