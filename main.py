import utime
from uPySensors.imu import MPU6050
from servo import Servo
from machine import Pin
import math
import umatrix

from madgwickahrs import MadgwickAHRS

sensor = MPU6050(0)

sensor.accel_range = 0
sensor.gyro_range = 1
sensor.filter_range = 1

ahrs = MadgwickAHRS(sampleperiod=0.150, beta=0.05)

# Servo specific constants
PULSE_MIN = 1.0  # in µs
PULSE_MAX = 2.0  # in µs
FREQUENCY = 50   # Hz
ROTATIONAL_RANGE_100 = math.pi
PIN0 = Pin.exp_board.G24
PIN1 = Pin.exp_board.G14

servo0 = Servo(PIN0, 0, FREQUENCY, ROTATIONAL_RANGE_100, PULSE_MIN, PULSE_MAX)
servo1 = Servo(PIN1, 1, FREQUENCY, ROTATIONAL_RANGE_100, PULSE_MIN, PULSE_MAX)

acc = []
gyro = []
while True:
    #start = utime.ticks_ms()
    accelerometer = sensor.accel
    gyrometer = sensor.gyro
    acc = umatrix.matrix([accelerometer.x, accelerometer.y, accelerometer.z], cstride=1, rstride=3, dtype=float)
    gyro = umatrix.matrix([gyrometer.x, gyrometer.y, gyrometer.z], cstride=1, rstride=3, dtype=float)

    #print("acceleration [X:%0.2f, Y:%0.2f, Z:%0.2f] gyro [X:%0.2f, Y:%0.2f, Z:%0.2f] \n"
    #        %(accelerometer.x, accelerometer.y, accelerometer.z, gyrometer.x * math.pi/180, gyrometer.y * math.pi/180, gyrometer.z * math.pi/180))

    #print("temperature [T:%0.2f]\n" %(sensor.temperature))

    ahrs.update_imu(gyro * math.pi/180.0, acc)

    (roll, pitch, yaw) = ahrs.quaternion.to_euler()

    print("roll: %0.2f, pitch: %0.2f yaw: %0.2f\n" %(roll, pitch, yaw))

    servo0.angle(math.pi/2 - pitch)
    servo1.angle(math.pi/2 + yaw)

    #print("Elapsed: %d" % (utime.ticks_ms() - start))
