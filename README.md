# uPyIMU

This code allows you to stabilize a camera using:
* IMU6050/IMU9255
* WiPy 2.0/3.0 (or ESP32)
* Micro Servos 9g
* Camera Tripod

The code uses the `ahrs` library from <a href="http://x-io.co.uk/open-source-imu-and-ahrs-algorithms/" target="_blank">Madgwick<i class="uk-icon-justify uk-icon-link"></i></a> which fusions the data of the accelerometer, gyroscope (and magnetometer, only with MPU9255) and allows to calculate the rotation of the IMU in quaternion coordinates.

## Connections
|   |
|:-:|
|<img src="https://raw.githubusercontent.com/lemariva/uPyIMU/master/fritzing/uPyMPU_bb.png" alt="WiPy 3.0, IMU6055 &amp; Micro Servo 9g" width="400px">|
|Fig. 1: WiPy, IMU6055 &amp; MicroServos|

### Cable description
|   |   |
|:-:|:-:|
|**Signal/Cable**|**Color**|
|5V | Red|
|GND| Black|
|3.3V| Yellow|

The 3.3V (yellow) is supplied by the WiPy board. The WiPy board needs 5V (top right pin or over USB). If you use the USB from your computer to power your WiPy, this 5V cannot be used for the servos! You need an external power supply!

## Revision
* v0.1 - initial commit

## More information
* [MicroPython: Camera stabilisation application!](https://lemariva.com/blog/2018/06/micropython-camera-stabilisation-application)

## Licenses
* check the files
