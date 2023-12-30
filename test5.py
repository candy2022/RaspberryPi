from flask import Flask, request, render_template
import time
import threading
import RPi.GPIO as GPIO

app = Flask(__name__)

LED = 7
KEY = 5
servoPin = 2

SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3
MAX_STATE_NUM = 3

btn_flag = False
btn_count = int(input("please input number: "))
cur_pos = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(KEY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 90)
servo.start(0)

def control_led(led_value):
    if led_value == '1':
        GPIO.output(LED, True)
        return 'ON'
    elif led_value == '2':
        GPIO.output(LED, False)
        return 'OFF'
    else:
        return ''

def servo_control(degree, delay):
    if degree > 180:
        degree = 180

    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    servo.ChangeDutyCycle(duty)
    time.sleep(delay)
    servo.ChangeDutyCycle(0)

def isr_key_event1(pin):
    global btn_flag, btn_count
    print("KeyD is pressed [%d]" % pin)
    btn_flag = True

GPIO.add_event_detect(KEY, GPIO.FALLING, callback=isr_key_event1, bouncetime=500)

def handle_direct_input():
    global btn_flag, btn_count, cur_pos
    while True:
        if btn_flag == True:
            btn_flag = False
            btn_count = (btn_count + 1) % MAX_STATE_NUM
            if btn_count == 0:
                GPIO.output(LED, True)
                time.sleep(0.3)
                GPIO.output(LED, False)
            elif btn_count == 1:
                GPIO.output(LED, True)
                time.sleep(1)
                GPIO.output(LED, False)
                time.sleep(1)
                GPIO.output(LED, True)
            else:
                GPIO.output(LED, False)
                cur_pos = cur_pos + 10
                if cur_pos > 180:
                    cur_pos = 180
                servo_control(cur_pos, 0.1)
                
        else:
            time.sleep(0.5)

button_thread = threading.Thread(target=handle_direct_input)
button_thread.daemon = True
button_thread.start()

@app.route('/test5')
def test3():
    global cur_pos
    cur_pos = 90
    servo_control(cur_pos, 0.1)
    return render_template('test5.html', degree=cur_pos)

@app.route('/ledtest', methods=['GET'])
def led_control_act():
    if request.method == 'GET':
        led_value = request.args.get("led")
        status = control_led(led_value)

    return render_template('test5.html', ret=status)

@app.route('/sg90_control_test', methods=['GET'])
def sg90_control_act():
    global cur_pos
    servo = request.args.get("servo")
    if servo == 'L':
        full_rotation()
    else:
        back_rotation()
    return render_template('test5.html', degree=cur_pos)

@app.route('/rbtn_control')
def rbtn_control():
    global btn_flag, btn_count, cur_pos
    btn_flag = True
    return render_template('test5.html', ret=cur_pos)

@app.route('/full_rotation', methods=['GET'])
def full_rotation():
    global cur_pos
    for i in range(1, 180, 10):
        cur_pos = i
        servo_control(i, 0.1)
        time.sleep(0.1)

@app.route('/back_rotation', methods=['GET'])
def back_rotation():
    global cur_pos
    for i in range(180, -1, -10):
        cur_pos = i
        servo_control(i, 0.1)
        time.sleep(0.1)

    return None

@app.route('/sg90_lcontrol_act')
def sg90_lcontrol_act():
    global cur_pos
    degree = ''
    cur_pos = cur_pos - 10
    if cur_pos < 0:
        cur_pos = 0
    servo_control(cur_pos, 0.1)
    return render_template('test5.html', ret=cur_pos)

if __name__ == '__main__':
    app.run(debug=False, threaded=True, port=80, host='0.0.0.0')
    GPIO.cleanup()
