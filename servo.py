# coding=utf-8
'''
 Copyright [2017] [Mauro Riva <lemariva@mail.com> <lemariva.com>]

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
'''

from machine import Pin, PWM
from uos import uname
PERC_100 = 10000  # in 100% * 100

class Servo:
    """
    WiPy servo object
    Sets up Timer and Channel and performs calculation so servo angle is automatically converted to duty cycle.
    """

    def __init__(self, gp_pin, channel, frequency, full_range100, pulse_min, pulse_max):
        """
        :param gp_pin: GPIO pin
        :channel: PWM unit
        :param frequency: in Hz
        :param full_range100: in deg
        :param pulse_min: in µs (WiPy3.0) in Duty (for ESP32, it should be - 30)
        :param pulse_max: in µs (WiPy3.0) in Duty (for ESP32, it should be - 30)
        :return:
        """

        # Store object properties
        self.PWM_frame = frequency  # in Hz
        self.full_range100 = full_range100
        self.pulse_min = pulse_min
        self.pulse_diff = pulse_max - pulse_min

    	self.min_position = 0
    	self.max_position = 180

        if (uname().sysname == 'WiPy'):
        	# Configure PWM timer to pin flow
        	self.pwm = PWM(0, frequency=self.PWM_frame)
        	self.servo = self.pwm.channel(channel, pin=gp_pin, duty_cycle=0.077)  # initial duty cycle of 7.5%
        else:
            self.pwm = PWM(gp_pin, freq=self.PWM_frame)

    def angle(self, angle100):
        """
        Set timer duty cycle to specified angle
        :param angle100: angle in deg * 100
        :return:
        """
        angle_fraction = float(angle100) / float(self.full_range100)
        pulse_width = float(self.pulse_min + angle_fraction * self.pulse_diff) # in µs
        if (uname().sysname == 'WiPy'):
            duty_cycle =  pulse_width * 100 / (1000 / self.PWM_frame) / 100
            self.servo.duty_cycle(duty_cycle)
        else:
            self.pwm.duty(int(pulse_width))
