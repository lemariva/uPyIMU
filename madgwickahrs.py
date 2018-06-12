# -*- coding: utf-8 -*-
"""
    Copyright (c) 2015 Jonas Böer, jonas.boeer@student.kit.edu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
import umatrix
import ulinalg
from quaternion import Quaternion


class MadgwickAHRS:
    samplePeriod = 1/100
    quaternion = Quaternion(1, 0, 0, 0)
    beta = 1.0

    def __init__(self, sampleperiod=None, quaternion=None, beta=None):
        """
        Initialize the class with the given parameters.
        :param sampleperiod: The sample period
        :param quaternion: Initial quaternion
        :param beta: Algorithm gain beta
        :return:
        """
        if sampleperiod is not None:
            self.samplePeriod = sampleperiod
        if quaternion is not None:
            self.quaternion = quaternion
        if beta is not None:
            self.beta = beta

    def update(self, gyroscope, accelerometer, magnetometer):
        """
        Perform one update step with data from a AHRS sensor array
        :param gyroscope: A three-element array containing the gyroscope data in radians per second.
        :param accelerometer: A three-element array containing the accelerometer data. Can be any unit since a normalized value is used.
        :param magnetometer: A three-element array containing the magnetometer data. Can be any unit since a normalized value is used.
        :return:
        """
        q = self.quaternion

        # Normalise accelerometer measurement
        if ulinalg.norm(accelerometer) is 0:
            print("accelerometer is zero")
            return
        accelerometer = accelerometer / ulinalg.norm(accelerometer)

        # Normalise magnetometer measurement
        if ulinalg.norm(magnetometer) is 0:
            print("magnetometer is zero")
            return
        magnetometer = magnetometer / ulinalg.norm(magnetometer)

        h = q * (Quaternion(0, magnetometer[0,0], magnetometer[0,1], magnetometer[0,2]) * q.conj())
        b = [0, ulinalg.norm(h[1:3]), 0, h[3]]

        # Gradient descent algorithm corrective step
        f = umatrix.matrix(
            [ 2*(q[1]*q[3] - q[0]*q[2]) - accelerometer[0,0],
              2*(q[0]*q[1] + q[2]*q[3]) - accelerometer[0,1],
              2*(0.5 - q[1]**2 - q[2]**2) - accelerometer[0,2],
              2*b[1]*(0.5 - q[2]**2 - q[3]**2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]) - magnetometer[0,0],
              2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]) - magnetometer[0,1],
              2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]**2 - q[2]**2) - magnetometer[0,2]
            ], cstride=1, rstride=1, dtype=float)
        j = umatrix.matrix(
            [ [-2*q[2],                  2*q[3],                  -2*q[0],                  2*q[1]],
              [2*q[1],                   2*q[0],                  2*q[3],                   2*q[2]],
              [0,                        -4*q[1],                 -4*q[2],                  0],
              [-2*b[3]*q[2],             2*b[3]*q[3],             -4*b[1]*q[2]-2*b[3]*q[0], -4*b[1]*q[3]+2*b[3]*q[1]],
              [-2*b[1]*q[3]+2*b[3]*q[1], 2*b[1]*q[2]+2*b[3]*q[0], 2*b[1]*q[1]+2*b[3]*q[3],  -2*b[1]*q[0]+2*b[3]*q[2]],
              [2*b[1]*q[2],              2*b[1]*q[3]-4*b[3]*q[1], 2*b[1]*q[0]-4*b[3]*q[2],  2*b[1]*q[1]]
            ], cstride=1, rstride=4, dtype=float)

        step = ulinalg.dot(j.transpose(), f)
        step = step / ulinalg.norm(step)  # normalise step magnitude

        # Compute rate of change of quaternion
        qdot = (q * Quaternion(0, gyroscope[0,0], gyroscope[0,1], gyroscope[0,2])) * 0.5 -  Quaternion(step.transpose() * self.beta)

        # Integrate to yield quaternion
        q = q + qdot * self.samplePeriod
        self.quaternion = q * (1 / ulinalg.norm(q._q))  # normalise quaternion

    def update_imu(self, gyroscope, accelerometer):
        """
        Perform one update step with data from a IMU sensor array
        :param gyroscope: A three-element array containing the gyroscope data in radians per second.
        :param accelerometer: A three-element array containing the accelerometer data. Can be any unit since a normalized value is used.
        """
        q = self.quaternion

        # Normalise accelerometer measurement
        if ulinalg.norm(accelerometer) is 0:
            print("accelerometer is zero")
            return
        accelerometer = accelerometer / ulinalg.norm(accelerometer)

        # Gradient descent algorithm corrective step
        f = umatrix.matrix(
            [ 2*(q[1]*q[3] - q[0]*q[2]) - accelerometer[0,0],
              2*(q[0]*q[1] + q[2]*q[3]) - accelerometer[0,1],
              2*(0.5 - q[1]**2 - q[2]**2) - accelerometer[0,2] ], cstride=1, rstride=1, dtype=float)

        j = umatrix.matrix(
             [ -2*q[2], 2*q[3], -2*q[0], 2*q[1],
                2*q[1], 2*q[0], 2*q[3], 2*q[2],
                0, -4*q[1], -4*q[2], 0 ], cstride=1, rstride=4, dtype=float)

        step = ulinalg.dot(j.transpose(), f)
        step = step / ulinalg.norm(step)  # normalise step magnitude

        # Compute rate of change of quaternion
        qdot = (q * Quaternion(0, gyroscope[0,0], gyroscope[0,1], gyroscope[0,2])) * 0.5 - Quaternion(step.T * self.beta)

        # Integrate to yield quaternion
        q = q + qdot * (self.samplePeriod)
        self.quaternion = q * (1 / ulinalg.norm(q._q))  # normalise quaternion
