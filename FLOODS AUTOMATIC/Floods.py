import RPi.GPIO as GPIO
import time
from gpiozero import Servo
from time import sleep

# Konfigurasi pin
TRIG_PIN = 9
ECHO_PIN = 10
SERVO_PIN = 3

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

try:
    my_servo = Servo(SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)
except Exception as e:
    print("Gagal menginisialisasi servo:", e)
    GPIO.cleanup()
    exit()

def baca_jarak(timeout=0.02):
    
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.0002)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # echo start
    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        if time.time() - start_time > timeout:
            return None  # Timeout
        pulse_start = time.time()

    # echo done
    while GPIO.input(ECHO_PIN) == 1:
        if time.time() - pulse_start > timeout:
            return None  # Timeout
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance_cm = (pulse_duration * 34300) / 2

    return distance_cm

def kontrol_servo(distance):
    if distance is None:
        print("Sensor error atau tidak ada pantulan.")
        return
    print(f"Jarak dari sensor ke air: {distance:.2f} cm")

    if distance > 20:
        my_servo.min()  # posisi tertutup
    elif 10 < distance <= 20:
        my_servo.value = 0  # posisi setengah buka
    elif distance <= 10:
        my_servo.max()  # posisi terbuka penuh
    else:
        print("Data tidak valid.")

try:
    while True:
        jarak = baca_jarak()
        kontrol_servo(jarak)
        sleep(0.5)

except KeyboardInterrupt:
    print("Program dihentikan oleh user.")

finally:
    GPIO.cleanup()