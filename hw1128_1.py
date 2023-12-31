# 1) 버튼을 1번 클릭하면 DC 모터가 정방향으로 10~60%까지 가속되면서 회전을 하고, 한번 더 클릭하면 역방향으로 10-60%까지 속도가 증가하고, 세번째 클릭하면 모터가 정지합니다.  
import RPi.GPIO as GPIO
import time
MOTOR_P = 20 # DC모터 핀 번호 
MOTOR_M = 21
KEY = 5 # 버튼 핀 번호 
a = 0 

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN)
GPIO.setup(MOTOR_P, GPIO.OUT)
GPIO.setup(MOTOR_M, GPIO.OUT)

def event(pin):
    print("key press [%d] "%pin)
    global a

    if a == 0: 
        a += 1
        pwm_m.ChangeDutyCycle(0)
        for i in range(10, 60): # 모터 가속 
            pwm_p.ChangeDutyCycle(i)
        time.sleep(0.1) #0.1초 지연 
        
    elif a == 1:
        a += 1
        for i in range(60, 10, -1): #서서히 감속 
            pwm_p.ChangeDutyCycle(i)
        time.sleep(0.1)
        pwm_p.ChangeDutyCycle(0)
        for i in range(10, 60): # 반대 방향으로 가속 
            pwm_m.ChangeDutyCycle(i)
        time.sleep(0.1)

    elif a == 2:
        pwm_p.ChangeDutyCycle(0)
        pwm_p.ChangeDutyCycle(0)
        a = 0

GPIO.add_event_detect(KEY,GPIO.FALLING,callback=event, bouncetime=300) 

try:
    pwm_p = GPIO.PWM(MOTOR_P, 100)
    pwm_m = GPIO.PWM(MOTOR_M, 100)
    pwm_p.start(0)
    pwm_m.start(0)

    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    pass
finally:

    pwm_m.stop()
    pwm_p.stop()
    GPIO.cleanup()
