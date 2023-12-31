# 한번 버튼을 클릭하면, 0~170도 까지 10도씩 증가하면서 회전하고, 다시 버튼을 누르면 170~0도까지 10도씩 감소하면서 역으로 회전하도록 합니다.
import RPi.GPIO as GPIO
import time
servoPin = 2 #서보모터 핀 번호 
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3
KEY = 5 # 버튼 핀 번호 
a = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(KEY, GPIO.IN)
servo = GPIO.PWM(servoPin, 50)
servo.start(0)

def servo_control(degree, delay):
    if degree > 170:
        degree = 170
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 170.0)
    print("Degree: {} to {}(Duty)".format(degree, duty))
    servo.ChangeDutyCycle(duty)
    time.sleep(delay)

def event(pin):
    global a
    print("button press [%d]"%pin)

    if a == 1:
        a = 0
        for i in range(1, 170, 10):
            servo_control(i, 0.1)
    elif a == 0:
        a = 1
        for i in range(170, 0, -10):
            servo_control(i, 0.1)
 
GPIO.add_event_detect(KEY,GPIO.FALLING, callback=event, bouncetime=100) # 인터럽트 사용 

try:
    while True:
       time.sleep(2)
 
except KeyboardInterrupt:
    pass
finally:
    servo.stop()
    GPIO.cleanup()
