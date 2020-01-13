# 약 배달 로봇
시간에 맞춰 병실을 돌며 환자에게 약을 배달하는 로봇을 만드는 프로젝트
<br>
<br>
<br>

## **문서 수정 사항**
-------------------------

 | **날짜**     |**수정자**   |**내용**                                       | **비고** |
 | ------------ |------------ |-----------------------------------------------| ----------|
 | 2020.01.09   |팀원 전체    |논의 된 내용을 바탕으로 각각 담당을 맡아 정리   |v1.0|

<br>
<br>
<br>

## **INDEX**
-------------------------

**[INTRODUCTION](#introduction)**

**[SERVICE SCENARIO](#service-scenario)**

**[REQUIREMENTS](#requirements)**

**[SYSTEM OVERVIEW](#section)**

**[FLOW CHART](#flow-chart)**

**[PRODUCT FUNCTIONS](#product-functions)**

**[HARDWARE INTERFACE](#section-1)**

**[APPENDIX \[하드웨어 스펙\]](#appendix-하드웨어-스펙)**

**[APPENDIX \[병원 내 환자 안전\]](#appendix-병원-내-환자-안전)**

**[APPENDIX \[그 외 추가 논의 사항\]](#appendix-그-외-추가-논의-사항)**

<br>
<br>
<br>

## **INTRODUCTION**
----------------------------

로봇은 인간의 개입없이 자동적으로 작동하도록 프로그램된 기계로, 핵심
키워드는 '자율성'이다.

그렇기 때문에 자율주행 자동차, 자율비행 드론 등
물리적인 장치를 갖추고서 컴퓨터 프로그램에 의해 자동적으로 작동함으로써
주어진 작업을 수행하는 기계들은 모두 로봇의 범위에 속한다.

최근, 로봇과
관련된 업계에서 '배달 로봇(Delivery Robot)이 화두로 떠오르고 있다.
아마존, 배달의 민족 등 실제 현업에서 배달 로봇을 사용하고 있다.
조사[^1]에 따르면 서비스 로봇의 시장 규모는 2018년 112억 달러에서 2023년
297억 달러로 연평균 21.44% 성장할 것으로 예상됐다.

![그림 1. 시도별 전국 의료 인력](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EC%8B%9C%EB%8F%84%EB%B3%84%20%EC%A0%84%EA%B5%AD%20%EC%9D%98%EB%A3%8C%20%EC%9D%B8%EB%A0%A5.jpg?raw=true)
![그림 2. 시도별 전국 의료기관](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EC%8B%9C%EB%8F%84%EB%B3%84%20%EC%A0%84%EA%B5%AD%20%EC%9D%98%EB%A3%8C%EA%B8%B0%EA%B4%80%20%ED%98%84%ED%99%A9.jpg?raw=true)

\<그림 1. 시도별 전국 의료 인력\> \<그림 2. 시도별 전국 의료기관 현황\>

그림 1과 그림 2로 지역별 의료 인력 편차가 큰 것을 확인할 수 있다.

전체 의료 기관 중 서울에 위치한 의료기관은 12.03%, 인력은 전체 중 서울에
24.89% 위치해 있지만 부산에는 전체 의료 기관 중 10.81%가 위치해 있고,
8.01%로 의료기관의 분포에 비해 의료 종사자의 분포가 적음을 알 수 있다.

이러한 인력 문제를 해결하기 위해 단순 업무들을 대신하는 스마트 의료
서비스 로봇을 제공한다. 그리고 이 서비스를 통해 생기는 여유 인력을 의료
종사자가 부족한 곳에서도 조금 더 원활하게 일이 돌아갈 수 있도록 하고자
한다.

<br>
<br>
<br>
<br>

## **SERVICE SCENARIO** 
----------------------------
<br>
<br>

| 구성 요소   | 설명                                                  |
|-------------|-------------------------------------------------------|
| 사용자 그룹 | 지방에 있는 대학 병원에서 일하는 간호사               |
| 시놉시스    | 간호사A씨는 지방에 있는 대학병원에 다닌다.<br> 환자 수에 비해 일하는 간호사의 수가 적다.<br>입원해 있는 많은 환자들에게 시간에 맞추어 약을      전달해야 되는 등의 단순 작업으로 쉴새 없이 바쁘다.<br>여유가 없어 환자들에게 질 좋은 서비스를 제공하지 못해 아쉽다. |
| 니즈        | 환자들에게 좀 더 질 좋은 서비스를 제공하고 싶다.      |
| 불편사항    | 단순 반복 노동이 많아 시간적 여유가 없다.             |
| 대안마련    | 단순 작업을 자동화한 로봇을 이용하여 업무의 효율성을 높인다.|
| 서비스 구성 | 약 배달 로봇                                          |

<br>
<br>
<br>
<br>

## **REQUIREMENTS**
-----------------

\*SA=Safety P=Performance SE=Security

<br>

| 요구사항 P-001 | 환자 처방 맞춤형 로봇 주행                         |
|---------------|--------------------------------------------------|
| 상세 설명      | 환자 맞춤형 약 배달을 위해<br>1 환자 정보를 서버로부터 내려받는다.<br> 1.1 환자 정보를 내려 받을 때 방문할 다음 병실의 환자 정보만을 받는다.<br> 1.2 방문 완료 시에는 내려 받은 환자 정보를 삭제한다. <br> 2 시간에 맞추어 해당 병실 앞으로 이동<br> 3 해당 환자에게 약을 전달한다|
||

<br>

| 요구사항 SA-001 | 환자 이중 확인                                    |
|--------------|--------------------------------------------------|
| 상세 설명       | 기존의 환자 확인 절차를 따라<br> 1 개방형 질문을 통한 환자의 참여를 요구<br> 2 최소한 2가지 이상의 지표를 사용하여 환자를 확인 |
||

<br>

| 요구사항 SE-001 | 로봇 도난 방지                                           |
|--------------|--------------------------------------------------|
| 상세 설명       | 정해진 시간 외에 일정 시간 정해진 위치에서 벗어났을 경우<br>1 경고음 발생<br>2 담당자에게 연락|
||

<br>
<br>
<br>
<br>

## **SYSTEM OVERVIEW**
-------------------------

다음 그림 3과 그림 4는 입원 환자에게 약 배달을 하는 모빌리티의 시스템
구성도 이다.

![그림 3. 프로토 타입 로봇](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%ED%94%84%EB%A1%9C%ED%86%A0%20%ED%83%80%EC%9E%85%20%EB%A1%9C%EB%B4%87.jpg?raw=true)

\<그림 3. 프로토 타입 로봇\>

![그림 4. 시스템 개요](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EC%9A%94.jpg?raw=true)

\<그림 4. 시스템 개요\>

<br>
<br>
<br>
<br>

## **FLOW CHART**
---------------

다음 그림은 로봇이 환자에게 약을 배달하기위한 과정을 간략하게 흐름도로
나타낸 것이다.

해당 흐름도에서 나타나 있지 않은 부분은 환자가 병실에 없을 경우, 간호사가 부족한 약을 보충하기 위해 로봇을 호출하였을 경우에 대한 흐름이 빠져있다. 해당 부분은 추후 논의를 통해 추가하고자 한다.

자세한 사항은 APPENDIX \[그 외 추가 논의사항\]을 참고

![그림 5. 약 배달 흐름도](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EC%95%BD%EB%B0%B0%EB%8B%AC%20%ED%9D%90%EB%A6%84%EB%8F%84.jpg?raw=true)

\<그림 5. 약 배달 흐름도\>

<br>
<br>
<br>
<br>

## **PRODUCT FUNCTIONS**
----------------

### 1. 로봇 주행  
처방된 약을 환자에게 배달하기 위해 정해진 길을 따라 주행한다.

  |함수 명                                 |설명
  |---------------------------------------|----|
  |advanced\_straight\_edge\_detection()   |직선검출을 위하여 관심영역 ROI를 설정하고 ROI 내 검사선들의 이미지 값의 구배 변화를 측정하여 추측되는 직선을 반환한다.|
  |line\_tracing()                         |환자들에게 약을 전달하기 위해 검출된 선을 따라 한 바퀴 주행한다.|
  |cal\_homography()                       |영상 이미지 픽셀 좌표계를 플랫폼 구동 축 중심의 좌표계로 변환|
  |move\_to\_patient()                     |cal\_homography()에서 계산된 환자의 좌표로 이동|
  ||

### 2. 환자 식별 - 안면 인식   
이 시스템에서는 환자를 식별하기 위해 안면 인식과 음성 인식 2가지 방법을 사용한다. <br>안면 인식은 Open CV와 AI를 이용한다.

  |함수 명           |설명|
  |----------------- |--------------------------------------------|
  |find\_patient()   |약을 전달해주기 위한 환자의 얼굴을 찾는다.|
  ||

### 3. 환자 식별 - 음성 인식  
음성 인식은 구글 인공지능 음성인식 및 출력 키트인 Voice Kit을 사용한다.<br>
이 기능에서는 안면 인식을 통해 식별된 환자의 이름을 호출하고 응답을 통해 2차 인증을 한다.

  |함수 명             |설명|
  |-------------------|----|
  |verify\_patient()   |안면인식을 통해 식별된 앞에 있는 환자의 이름을 호출하고 응답을 받아 2차 인증을 한다.|
  |notify\_patient()   |환자에게 주의사항을 알려준다.|
||

### 4. 환자 정보 및 처방 약 데이터 베이스

약을 제공하는 과정에서 환자와 처방 된 약의 정보를 담고있는 데이터베이스를 처리하는 기능들이다.

  |함수 명                          |설명|
  |--------------------------------|----|
  |get\_patient\_info()             |환자의 이름, 생년월일, 등록번호 등 환자 확인을 위한 정보를 서버로 부터 받는다.|
  |get\_patient\_face\_info()       |얼굴 인식을 위한 환자 얼굴정보를 서버로부터 받는다.|
  |update\_prescription\_record()   |환자가 처방된 약을 받았는지 true/false DB 업데이트|
  |search\_prescription\_record()   |환자 데이터베이스로 부터 약을 받지 못한/약을 받은 환자 정보 가져오기|
||

### 5.  로봇 제어

환자에게 처방된 약을 전달하기 위한 로봇 제어가 필요하다. <br>
로봇제어에 필요한 센서에는 각도 조절을 위한 Servo motor, 장애물 감지를 위한 Ultrasonic sensor, cover를 열기 위한 switch가 있다.

<br>

| 함수명             | 설명                                           |
|--------------------|------------------------------------------------|
| open\_cover()      | 의료진이 로봇에 약을 채워줄 경우에 버튼을 눌러 button digital value가 1이 되면, 뚜껑이 열리도록 한다.  <br>switch 사용|
| choose\_drug()     | 로봇 내부에 있는 약을 로봇팔로 전달하기 위해 servo에 의해 약을 가로막는 커버를 열어 로봇팔쪽으로 전달될 수 있도록 하고, 전달이 완료되면 커버를 닫힐 수 있도록 한다. <br> servo motor 사용                   |
| obstacle\_detect() | Ultra sonic sensor에서 받아온 값을 이용하여 주행 하는 방향으로 특정 거리 이내에 물체 또는 사람이 감지되면 거리 내에 물체 또는 사람이 사라질 때까지 정지한다. <br>servo motor 사용                               |
||
<br>
<br>
<br>
<br>

## **HARDWARE INTERFACE**
---------------

이 로봇은 프로토 타입으로 안면인식과 병원 내 주행을 위한 카메라, 어두운
환경에서 카메라 센서의 에러를 줄이기 위한 IR 센서, 약을 보관하는 약품
보관함, 약통을 열기 위한 버튼, 이러한 센서들을 제어하기 위한 라즈베리
파이가 탑재되어 있다. 다음 그림 6을 통해 해당 센서들과 부품의 위치를
확인할 수 있다.

\<그림 6. 하드웨어 설계도\>
![](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EC%84%A4%EA%B3%84%EB%8F%84.jpg?raw=true)

\<그림 6. 하드웨어 설계도\>
<br>
<br>
<br>
<br>

## **APPENDIX \[하드웨어 스펙\]**
------------------------

-   Camera (Wide Angle Raspberry Pi Camera)

카메라로 영상을 받아와 Open CV로 영상처리 및 추가적인 머신러닝을
이용하여 안면인식을 한다.

![SainSmart Wide Angle Fish-Eye Camera Lenses for Raspberry Pi Arduino](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EC%96%B4%EC%95%88%EC%B9%B4%EB%A9%94%EB%9D%BC.jpg?raw=true)

\< SainSmart Wide Angle Fish-Eye Camera Lenses for Raspberry Pi Arduino\>

-   Outlet

환자의 처방약을 서버에서 받아와 제어부에서 제공한 약을 환자가 받을 수
있는 출입구이다. 버튼을 누르면 약 캐비넷을 볼 수 있다. 의료진은 환자가
필요한 약을 분류하여 배치시킨다.

![약 캐비넷](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EC%95%BD%20%EC%BA%90%EB%B9%84%EB%84%B7.jpg?raw=true)

-   Raspberry Pi Circuit

메인보드로서 총 제어를 담당한다.

![Raspberry Pi circuit](https://github.com/Aibia/NGV_MobilityProject/blob/master/img/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4.jpg?raw=true)

-   SoC: Broadcom BCM2837B0 quad-core A53 (ARMv8) 64-bit @ 1.4GHz

-   GPU: Broadcom Videocore-IV

-   RAM: 1GB LPDDR2 SDRAM

-   Networking: Gigabit Ethernet (via USB channel), 2.4GHz and 5GHz
    > 802.11b/g/n/ac Wi-Fi

-   Bluetooth: Bluetooth 4.2, Bluetooth Low Energy (BLE)

-   Storage: Micro-SD

-   GPIO: 40-pin GPIO header, populated

-   Ports: HDMI, 3.5mm analogue audio-video jack, 4x USB 2.0, Ethernet,
    > Camera Serial Interface (CSI), Display Serial Interface (DSI)

-   Dimensions: 82mm x 56mm x 19.5mm, 50g

<br>
<br>
<br>
<br>

## **APPENDIX \[병원 내 환자 안전\]**
---------------------------
### 1. 환자 안전

#### 가. 개념
  > 환자가 사고 손상으로부터 자유로운 상태 및 의료과오와 위해사건의 발생을
최소화하여 환자가 위해사건에 빠지지 않게 예방

#### 나. 환자안전의 중요성

>1\) 의료기관은 환자에게 안전하고 질 높은 서비스를 제공할 책임과 의무가
있으며, 병원 내에서 이루어지는 모든 과정에서 환자안전이 제일 우선으로
고려되어야 함
>
>2\) 병원 내 환자안전사고 발생시
>
> - 환자의 생명과 직결되는 치명적 결과 발생
> - 의료의 질 저하
> - 병원의 재정적 손실 발생
> - 원상회복이 어려움
> - 파급효과가 큼

### 2. 정확한 환자확인

#### 가. 목적
모든 진단과 치료과정에서 환자를 정확히 확인하여 환자에게 안전하고 정확한 치료와 서비스 제공

#### 나. 방법
>1. 개방형 질문 - "성함이 어떻게 되십니까?"
>1. 최소한 두 가지 이상의 지표(indicator)사용
>    1. 신분증이나 진료예약증, 진료카드 등에 기재된 환자이름과 등록번호 확인
>    1. 등록번호 확인이 어려운 경우 생년월일로 확인
>1. 환자의 병실호수나 위치를 알리는 지표는 환자확인 지표로 사용불가
>1. 모든 상황과 장소에서 일관된 환자확인 방법 적용
>1. 환자가 의식이 없거나 의사소통이 불가능한 경우
>-- 보호자에게 개방형으로 질문하여 확인

#### 다. 시점
>1. 의약품 투여 전
>1. 혈액제제 투여 전
>1. 검사 시행 전
>1. 진료 전
>1. 처치 및 시술 전

<br>
<br>
<br>
<br>

## **APPENDIX \[그 외 추가 논의 사항\]**
------------------------

-   안보이는(화장실 간, 누워있는, 사각지대) 환자의 위치 계산 혹은 언제 받게 할건지에 대한 문제

-   Audio Kit에 대한 인식률 테스트 후 하드웨어 부착 부위 찾기 문제

-   라즈베리파이와 오디오킷사이의 통신과 관련한 문제

[^1]: https://www.researchandmarkets.com/research/qfbt9n/top\_robotics?w=12

<br>
