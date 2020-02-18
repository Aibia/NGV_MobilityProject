#-*- coding:utf-8 -*-
import cv2
import numpy as np
import math
import time
import RPi.GPIO as GPIO
import signal
import sys
import Adafruit_PCA9685
from server import config
from server import logger
pwm = Adafruit_PCA9685.PCA9685()


MOTOR_STOP_PIN_NUM = config.MOTOR_STOP_PIN_NUM
SERVO_PIN_NUM = config.SERVO_PIN_NUM
MOTOR_PIN_NUM = config.MOTOR_PIN_NUM
COMMU_PIN_NUM = config.COMMU_PIN_NUM
SERVO_LEFT = config.SERVO_LEFT
SERVO_MID = config.SERVO_MID
SERVO_RIGHT = config.SERVO_RIGHT
## 가공 전 Steering Value
__SERVO_LEFT = config.__SERVO_LEFT
__SERVO_MID = config.__SERVO_MID
__SERVO_RIGHT = config.__SERVO_RIGHT
MOTOR_STOP = config.MOTOR_STOP
MOTOR_FORWARD = config.MOTOR_FORWARD
FIRST_FORWARD = config.FIRST_FORWARD
FIRST_MOTOR_FORWARD = config.FIRST_MOTOR_FORWARD
## DISPLAY CONFIG
DISPLAY_ON = config.DISPLAY_ON

GPIO.setmode(GPIO.BOARD)
pwm.set_pwm(SERVO_PIN_NUM, 0, SERVO_MID)

def detect_edges(frame):
    gray = cv2.cvtColor(frame, 6)
    mask = cv2.bilateralFilter(gray, 3, 15, 15, 4)
    # detect edges
    edges = cv2.Canny(mask, 100, 200)
    return edges


def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus lower half of the screen
    polygon = np.array([[
        (0, height),
        (0, height / 2),
        (width, height / 2),
        (width, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)

    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges


def detect_line_segments(cropped_edges):
    rho = 1
    theta = np.pi / 180
    min_threshold = 10

    line_segments = cv2.HoughLinesP(cropped_edges, rho, theta, min_threshold,
                                    np.array([]), minLineLength=5, maxLineGap=150)
    return line_segments


def average_slope_intercept(frame, line_segments):
    lane_lines = []

    if line_segments is None:
        logger.log.info("no line segments detected")
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1 / 3
    left_region_boundary = width * (1 - boundary)
    right_region_boundary = width * boundary

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                logger.log.info("skipping vertical lines (slope = infinity)")
                continue

            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)

            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    return lane_lines


def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line

    y1 = height  # bottom of the frame
    y2 = int(y1 / 2)  # make points from middle of the frame down

    if slope == 0:
        slope = 0.1

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [[x1, y1, x2, y2]]


def display_lines(frame, lines, line_color=(0, 255, 0), line_width=6):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)

    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape

    steering_angle_radian = steering_angle / 180.0 * math.pi

    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
    return heading_image


def get_steering_angle(frame, lane_lines):
    height, width, _ = frame.shape

    if len(lane_lines) == 2:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        mid = int(width / 2)
        x_offset = (left_x2 + right_x2) / 2 - mid
        y_offset = int(height / 2)
        num_lane = 2

    elif len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        mid = int(width / 2)
        x_offset = x2 - x1
        y_offset = int(height / 2)
        num_lane = 1

    elif len(lane_lines) == 0:
        x_offset = 0
        y_offset = int(height / 2)
        num_lane = 0

    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)
    steering_angle = angle_to_mid_deg + 90

    return steering_angle, num_lane

def stop_forwarding(sig, frame):
    pwm.set_pwm(MOTOR_PIN_NUM, 0 ,MOTOR_STOP)
    logger.log.info('Stopped!')
    sys.exit(0)

signal.signal(signal.SIGINT, stop_forwarding)

def run():
    before_angle = __SERVO_MID
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    time.sleep(1)

    pwm.set_pwm_freq(60)
    while True:
        while GPIO.gpio_function(MOTOR_STOP_PIN_NUM) == GPIO.OUT:
            pwm.set_pwm(MOTOR_PIN_NUM, 0, MOTOR_STOP)
            logger.log.info("Stopped !")
            time.sleep(1)
        _, frame = video.read()

        edges = detect_edges(frame)
        roi = region_of_interest(edges)
        line_segments = detect_line_segments(roi)
        lane_lines = average_slope_intercept(frame, line_segments)
        lane_lines_image = display_lines(frame, lane_lines)
        steering_angle, num_lane = get_steering_angle(frame, lane_lines)
        if DISPLAY_ON:
            heading_image = display_heading_line(lane_lines_image, steering_angle)
            cv2.imshow('video', heading_image)

        deviation = abs(steering_angle - before_angle)

        if deviation < 4:
            steering_angle = int((steering_angle + before_angle) / 2)
        elif deviation > 60:
            steering_angle = before_angle

        if num_lane == 0:
            steering_angle = before_angle

        before_angle = steering_angle
        logger.log.info("before_angle : {} steering_angle : {}".format(before_angle, steering_angle))
        pwm.set_pwm(MOTOR_PIN_NUM, 0, MOTOR_FORWARD)
        if steering_angle > __SERVO_RIGHT:
            steering_angle = __SERVO_RIGHT
        if steering_angle < __SERVO_LEFT:
            steering_angle = __SERVO_LEFT

        if steering_angle <= 100 and steering_angle >= 80:  #straight
            servo_pwm = steering_angle + 280
        elif steering_angle > 100:  #right
            servo_pwm = -0.0214 * steering_angle * 2 - 7.75 * steering_angle - 195
        else: #left
            servo_pwm = 0.0583 * steering_angle ** 2 - 4.1488 * steering_angle + 342.41

        pwm.set_pwm(SERVO_PIN_NUM, 0, int(servo_pwm))
        key = cv2.waitKey(1)
        if key == 27:
            break
    video.release()
    cv2.destroyAllWindows()