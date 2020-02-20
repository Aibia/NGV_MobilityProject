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
MOTOR_FORWARD_FASTER = config.MOTOR_FORWARD_FASTER

## DISPLAY CONFIG
DISPLAY_ON = config.DISPLAY_ON

GPIO.setmode(GPIO.BOARD)
pwm.set_pwm(SERVO_PIN_NUM, 0, SERVO_MID)

def detect_edges(frame):
    '''영상의 edge를 찾는 함수이다.
    영상을 흑백 이진화 처리한 후 bilateral filter를 이용하여 노이즈를 제거한다.
    Canny Algorithm을 이용해 edge를 찾는다.

    :param numpy.ndarray frame: 웹캠으로 입력받은 edge를 찾을 영상
    :returns numpy.ndarray edges: 영상의 edge
    '''
    gray = cv2.cvtColor(frame, 6)
    mask = cv2.bilateralFilter(gray, 3, 15, 15, 4)
    # detect edges
    edges = cv2.Canny(mask, 100, 200)
    return edges


def region_of_interest(edges):
    '''입력받은 영상의 하단 절반을 관심 영역으로 자른다.
    영상과 같은 크기의 array를 생성한 후 영상의 관심 영역 부분을 복사하여 반환한다.

    :param edges: 관심 영역을 지정할 edge를 찾은 영상
    :returns cropped_edges: 복사한 관심 영역 영상
    '''
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus lower half of the screen
    polygon = np.array([[
        (width / 5, height),
        (width / 5, height / 2),
        (4 * width / 5, height / 2),
        (4 * width / 5, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)

    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges


def detect_line_segments(cropped_edges):
    '''관심영역으로 자른 영상을 받아 차선으로 예상되는 선을 검출한다.
    입력 영상에서 임의의 점을 대상으로 차선을 검출하는 확률적 허프변환을 이용하여 차선을 찾는다.

    :param cropped_edges: 차선을 검출할 이진화된 영상
    :returns line_segments: 검출한 차선 윤곽선
    '''
    rho = 1
    theta = np.pi / 180
    min_threshold = 10

    line_segments = cv2.HoughLinesP(cropped_edges, rho, theta, min_threshold,
                                    np.array([]), minLineLength=5, maxLineGap=150)
    return line_segments


def average_slope_intercept(frame, line_segments):
    '''영상을 좌우 영역으로 나눠 양쪽 차선의 기울기와 y절편을 구한다.
    기울기가 음수일 경우 x1, x2 모두 왼쪽 영역에 있을때 왼쪽 차선,
    기울기가 음수가 아닐 경우 x1, x2 모두 오른쪽 영역에 있을때 오른쪽 차선으로 간주한다.
    이때 x1, x2가 같을 경우 수직이기에 건너뛴다.

    :param frame: 웹캠으로 입력받은 영상
    :param line_segments: 검출한 차선 윤곽선
    :returns lane_lines: 양측 차선
    '''
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
    '''웹캠 영상을 입력받아 좌표를 생성한다.
    기울기와 y절편으로 x좌표를 찾는다.
    이때, 기울기가 0인경우 0으로 나눌 수 없기 때문에 작은 값인 0.1로 대신 계산한다.

    * x1 : 차선의 왼쪽 가로 좌표
    * x2 : 차선의 오른쪽 가로 좌표
    * y1 : 영상 바닥 세로 좌표
    * y2 : 영상 높이의 중간 세로 좌표
    
    :param frame: 웹캠으로 입력받은 영상
    :param line: 왼쪽 또는 오른쪽 차선
    :returns:
    '''
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
    '''영상에 차선을 표시한다.

    :param frame: 웹캠으로 입력받은 영상
    :param lines: 차선
    :param line_color: 차선의 색
    :param line_width: 차선 두께
    :returns line_image: 차선이 표시된 영상
    '''
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)

    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5):
    '''차량의 steering angle을 직선으로 표시한다.
    
    :param frame: 웹캠으로 입력받은 영상
    :param steering_angle: 차량의 steering angle
    :param line_color: 표시할 직선의 색
    :param line_width: 표시할 직선의 두께
    :returns heading_image: steering angle이 표시된 영상
    '''
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
    '''웹캠에서 영상을 입력받아 steering angle을 구한다.
    차량이 양측 차선의 중앙으로 가도록 제어한다.
    입력 받은 영상에서 검출한 차선의 수에 따라 구한다.

    * x_offset : 양측 차선의 중간(가로축)과 화면 중앙의 차이
    * y_offset : 높이의 절반

    * 차선이 2개인 경우 : 두 차선의 중앙으로 향하도록 한다.
    * 차선이 1개인 경우 : 검출한 차선과 평행하도록 한다.

    :param frame: 웹캠으로 입력받은 영상
    :param int lane_lines: 차선의 수
    '''
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
    logger.log.info('[drive.py:stop_forwarding] Stopped!')
    sys.exit(0)

signal.signal(signal.SIGINT, stop_forwarding)


def run():
    MOTOR_STOP_FLAG = True
    if GPIO.gpio_function(MOTOR_STOP_PIN_NUM) == GPIO.OUT:
        MOTOR_STOP_FLAG = True

    before_angle = __SERVO_MID
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    time.sleep(1)

    pwm.set_pwm_freq(60)
    while True:
        while GPIO.gpio_function(MOTOR_STOP_PIN_NUM) == GPIO.OUT:
            MOTOR_STOP_FLAG = True
            pwm.set_pwm(MOTOR_PIN_NUM, 0, MOTOR_STOP)
            logger.log.info("[drive.py:run] Stopped GPIO Pin {} is GPIO.OUT!".format(MOTOR_STOP_PIN_NUM))
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

        '''
        deviation을 이용하여 oscillation(기준 4이하)을 잡아주고, outiler(기준 60이상)를 제거한다.
        이때, get_steering_angle에서 얻은 num_lane이 0일 경우 이전값으로 steering을 제어한다.

        *deviation : get_steering_angle에서의 steering_angle과 before_angle의 차
        '''
        deviation = abs(steering_angle - before_angle)

        if deviation > 60:
            steering_angle = before_angle

        if num_lane == 0:
            steering_angle = before_angle

        before_angle = steering_angle
        logger.log.info("[drive.py:run] before_angle : {} steering_angle : {}".format(before_angle, steering_angle))
        
        ## TODO 
        ## 여기가 위치가 맞는지.. 왜냐면 먼저 출발하고 스티어링을 하는게 맞는지
        ## 맞다면
        ## 
        if MOTOR_STOP_FLAG:
            ## 멈춰 있다 출발했을 경우 좀더 빠르게 출발 
            MOTOR_STOP_FLAG = False
            pwm.set_pwm(MOTOR_PIN_NUM, 0, MOTOR_FORWARD_FASTER)
        else:
            pwm.set_pwm(MOTOR_PIN_NUM, 0, MOTOR_FORWARD)
        
        if steering_angle > __SERVO_RIGHT:
            steering_angle = __SERVO_RIGHT
        if steering_angle < __SERVO_LEFT:
            steering_angle = __SERVO_LEFT

        '''
        * straight : 양 끝 값(100 / 80)에 가중치를 많이 두고 steering
        * right / left : 앞 부분에(100 - 115 / 65 - 80) 가중치를 많이 두고 steering
    
        * servo_pwm : 실제 차량을 제어하는 pwm값
        '''

        if steering_angle <= 96 and steering_angle >= 80:  #straight
            servo_pwm = 0.1372 * steering_angle ** 2 - 21.673 * steering_angle + 1210.6
        elif steering_angle > 96:  #right
            servo_pwm = -0.024 * steering_angle ** 2 + 7.769 * steering_angle - 136.82
        else: #left
            servo_pwm = 0.0334 * steering_angle ** 2 - 1.8034 * steering_angle + 287.71

        pwm.set_pwm(SERVO_PIN_NUM, 0, int(servo_pwm))
        key = cv2.waitKey(1)
        if key == 27:
            break
    video.release()
    cv2.destroyAllWindows()

    