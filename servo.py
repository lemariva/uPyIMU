# coding=utf-8
from machine import Pin, PWM
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
        :param pulse_min: in µs
        :param pulse_max: in µs
        :return:
        """

        # Store object properties
        self.PWM_frame = frequency  # in Hz
        self.full_range100 = full_range100
        self.pulse_min = pulse_min
        self.pulse_diff = pulse_max - pulse_min

    	self.min_position = 0
    	self.max_position = 180

    	# Configure PWM timer to pin flow
    	self.pwm = PWM(0, frequency=self.PWM_frame)
    	self.servo = self.pwm.channel(channel, pin=gp_pin, duty_cycle=0.077)  # initial duty cycle of 7.5%


    def angle(self, angle100):
        """
        Set timer duty cycle to specified angle
        :param angle100: angle in deg * 100
        :return:
        """
        angle_fraction = float(angle100) / float(self.full_range100)
        pulse_width = float(self.pulse_min + angle_fraction * self.pulse_diff) # in µs
        duty_cycle =  pulse_width * 100 / (1000 / self.PWM_frame) / 100
        self.servo.duty_cycle(duty_cycle)
