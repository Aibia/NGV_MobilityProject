# server.drive module


### server.drive.average_slope_intercept(frame, line_segments)
영상을 좌우 영역으로 나눠 양쪽 차선의 기울기와 y절편을 구한다.
기울기가 음수일 경우 x1, x2 모두 왼쪽 영역에 있을때 왼쪽 차선,
기울기가 음수가 아닐 경우 x1, x2 모두 오른쪽 영역에 있을때 오른쪽 차선으로 간주한다.
이때 x1, x2가 같을 경우 수직이기에 건너뛴다.


* **Parameters**

    
    * **frame** – 웹캠으로 입력받은 영상


    * **line_segments** – 검출한 차선 윤곽선



* **Returns lane_lines**

    양측 차선



### server.drive.detect_edges(frame)
영상의 edge를 찾는 함수이다.
영상을 흑백 이진화 처리한 후 bilateral filter를 이용하여 노이즈를 제거한다.
Canny Algorithm을 이용해 edge를 찾는다.


* **Parameters**

    **frame** (*numpy.ndarray*) – 웹캠으로 입력받은 edge를 찾을 영상



* **Returns numpy.ndarray edges**

    영상의 edge



### server.drive.detect_line_segments(cropped_edges)
관심영역으로 자른 영상을 받아 차선으로 예상되는 선을 검출한다.
입력 영상에서 임의의 점을 대상으로 차선을 검출하는 확률적 허프변환을 이용하여 차선을 찾는다.


* **Parameters**

    **cropped_edges** – 차선을 검출할 이진화된 영상



* **Returns line_segments**

    검출한 차선 윤곽선



### server.drive.display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5)
차량의 steering angle을 직선으로 표시한다.


* **Parameters**

    
    * **frame** – 웹캠으로 입력받은 영상


    * **steering_angle** – 차량의 steering angle


    * **line_color** – 표시할 직선의 색


    * **line_width** – 표시할 직선의 두께



* **Returns heading_image**

    steering angle이 표시된 영상



### server.drive.display_lines(frame, lines, line_color=(0, 255, 0), line_width=6)
영상에 차선을 표시한다.


* **Parameters**

    
    * **frame** – 웹캠으로 입력받은 영상


    * **lines** – 차선


    * **line_color** – 차선의 색


    * **line_width** – 차선 두께



* **Returns line_image**

    차선이 표시된 영상



### server.drive.get_steering_angle(frame, lane_lines)
웹캠에서 영상을 입력받아 steering angle을 구한다.
차량이 양측 차선의 중앙으로 가도록 제어한다.
입력 받은 영상에서 검출한 차선의 수에 따라 구한다.


* x_offset : 양측 차선의 중간(가로축)과 화면 중앙의 차이


* y_offset : 높이의 절반


* 차선이 2개인 경우 : 두 차선의 중앙으로 향하도록 한다.


* 차선이 1개인 경우 : 검출한 차선과 평행하도록 한다.


* **Parameters**

    
    * **frame** – 웹캠으로 입력받은 영상


    * **lane_lines** (*int*) – 차선의 수



### server.drive.make_points(frame, line)
웹캠 영상을 입력받아 좌표를 생성한다.
기울기와 y절편으로 x좌표를 찾는다.
이때, 기울기가 0인경우 0으로 나눌 수 없기 때문에 작은 값인 0.1로 대신 계산한다.


* x1 : 차선의 왼쪽 가로 좌표


* x2 : 차선의 오른쪽 가로 좌표


* y1 : 영상 바닥 세로 좌표


* y2 : 영상 높이의 중간 세로 좌표


* **Parameters**

    
    * **frame** – 웹캠으로 입력받은 영상


    * **line** – 왼쪽 또는 오른쪽 차선



* **Returns**

    


### server.drive.region_of_interest(edges)
입력받은 영상의 하단 절반을 관심 영역으로 자른다.
영상과 같은 크기의 array를 생성한 후 영상의 관심 영역 부분을 복사하여 반환한다.


* **Parameters**

    **edges** – 관심 영역을 지정할 edge를 찾은 영상



* **Returns cropped_edges**

    복사한 관심 영역 영상



### server.drive.run()

### server.drive.stop_forwarding(sig, frame)
