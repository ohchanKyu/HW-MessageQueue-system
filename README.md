# MessageQueue-System

## HW 개요
해당 어플리케이션은 Python과 ZeroMQ를 기반으로 설계되었으며, <br>
두 가지 주요 통신 패턴을 활용하여 클라이언트와 서버 간의 상호작용을 지원합니다. <br>
두 가지의 통신 패턴은 Request-Reply와 Publish-Subscribe 패턴이며, <br>
이를 통해 클라이언트는 서버와 요청-응답을 주고받으며 초기 설정을 구성하고, <br>
구독을 통한 실시간 업데이트 수신 및 이메일을 통해 업데이트 내역을 받을 수 있습니다. <br>

<br>

## ZeroMQ 기반 메시징 시스템 구성
#### Request-Reply + Publish-Subscribe 패턴 결합
이 애플리케이션은 Request-Reply로 초기 설정 요청을 받고, <br>
Publish-Subscribe를 통해 실시간 업데이트를 수신하는 구조입니다. <br>
두 패턴은 서로 다른 포트를 사용해 독립적으로 동작하며, ZeroMQ의 패턴을 효율적으로 최적화합니다. <br>

<br>

#### 비동기 전송으로 실시간 알림 최적화
ZeroMQ는 비동기 메시징을 지원하여, 서버가 다수의 구독자에게 실시간으로 콘텐츠 변경 사항을 빠르게 전달합니다. <br>
구독자가 많아져도 서버 부하가 적고 대기 시간이 짧아 실시간 알림 시스템에 최적화되어 있습니다. <br>

<br>

#### 주제 기반 필터링 지원
ZeroMQ의 PUB-SUB 구조는 주제 기반 필터링을 지원합니다. <br>
구독자는 원하는 주제만 선택해 필요한 데이터만 수신하므로, <br>
네트워크 효율성과 사용자 맞춤 경험을 모두 달성할 수 있습니다. <br>

<br>

## **Directory**
```
📦MessageQueueClient
 ┗ 📜main.py
📦MessageQueueServer
 ┣ 📜EmailHandler.py
 ┣ 📜main.py
 ┣ 📜StoreContext.py
 ┣ 📜ZmqPublisher.py
 ┗ 📜ZmqServer.py
```

<br>

## 애플리케이션 시나리오

**1️⃣ Request-Reply 패턴: 초기 설정 및 구독 요청** <br>
클라이언트는 Request-Reply 패턴을 통해 서버에 연결하여 다음 작업을 수행합니다 <br>
- 구독 가능한 콘텐츠 목록 조회 <br>
- 콘텐츠 구독 신청 <br>
- 이메일 주소 등록 <br>

클라이언트의 요청에 대해 서버는 순차적으로 응답을 반환하며, 초기 설정을 마무리합니다. <br>

<br>

**2️⃣ Publish-Subscribe 패턴: 실시간 콘텐츠 업데이트** <br>
사용자가 콘텐츠를 구독하면, 클라이언트는 SUB 소켓을 별도 스레드로 실행하고, <br>
서버의 PUB 소켓과 연결하여 실시간 업데이트를 수신합니다. <br>
- 서버는 콘텐츠에 변화가 있을 때마다 PUBLISH 메시지 전송 <br>
- 클라이언트는 해당 콘텐츠에 대해 비동기적으로 메시지를 수신 <br>
- 각 구독자는 자신의 관심 주제에만 반응하도록 구성됨 <br>

<br>

**3️⃣ 이메일 알림 서비스** <br>
구독자가 등록한 이메일을 기반으로, 콘텐츠에 변경이 발생할 경우 이메일 알림이 발송됩니다. <br>
- 서버는 업데이트 발생 시 이메일 발송을 위한 메시지를 처리 <br>
- EmailHandler 클래스를 통해 SMTP로 이메일 전송 <br>
- 구독자는 이메일을 통해 콘텐츠 변경 사항을 실시간으로 확인 가능 <br>

<br>

## **Settings**
### Ubuntu 기본 환경 구축
#### 사용자 홈 디렉토리로 이동 및 패키지 목록 업데이트
```Bash
cd ~
sudo apt update
```
#### Python pip / zeroMQ 설치
```Bash
sudo apt-get install python3-pip
pip3 install pyzmq
```
#### 프로젝트 clone 및 해당 프로젝트로 이동
```Bash
git clone https://github.com/ohchanKyu/HW-MessageQueue-system.git
cd ./HW-MessageQueue-system
```

<br>

### 애플리케이션 실행
#### 서버 애플리케이션 실행
```Bash
python3 ./MessageQueueServer/main.py
```
#### 클라이언트 애플리케이션 실행
```Bash
python3 ./MessageQueueClient/main.py
```

<br>

## **Test Application**
**[클라이언트 초기 화면]** <br>
![image](https://github.com/user-attachments/assets/3c0a4728-7e6c-4159-ac12-fdf159e9e34d)

<br>

**[클라이언트 Command 1번]** <br>
- 클라이언트는 서버에게 구독 가능한 리스트 요청
- 서버는 클라이언트에게 리스트 메세지로 응답
![image](https://github.com/user-attachments/assets/a233e9c8-11f7-4448-822a-0ad96d4c8963)
- 리스트 요청을 받은 서버쪽 출력
![image](https://github.com/user-attachments/assets/510ce449-8f7b-4d85-9440-201035906287)

<br>

**[클라이언트 Command 2번]** <br>
- 서버에게 구독을 요청 ( SpringBoot / NodeJs / React / Django 중 1가지 선택 )
- 구독할 Subject와 이메일 입력
- 서버는 해당 Subject와 Email을 전달받고 응답 메세지를 생성
- 메시지 응답으로 구독한 Subject 및 Subject에 대한 Content를 전달
![image](https://github.com/user-attachments/assets/8225dd8b-aef5-46ee-a7f5-d8cebb4a78b4)
- 구독 요청을 받은 서버쪽 출력
![image](https://github.com/user-attachments/assets/cdbaa68f-c158-4e27-a002-6788ea0ab24a)

<br>

**[클라이언트 Command 3번]** <br>
﻿- 클라이언트 측에서 구독한 Subject에 대해 내용을 추가
- 서버측에서는 해당 요청을 받고, 모든 구독자들에게 메시지 전달 및 이메일 전송
![image](https://github.com/user-attachments/assets/abeeec1a-a51a-4194-a23a-731d187c44c8)
- 실제로 받은 이메일 화면
![image](https://github.com/user-attachments/assets/553b2d6b-a0b0-4b2e-bf78-ec63dba0b426)

<br>

**[클라이언트 Command 4번]** <br>
- 클라이언트에게 기존의 메뉴를 다시 출력
![image](https://github.com/user-attachments/assets/e22aa1a5-535e-41b6-9b01-0e737e4fbc69)

<br>

**[클라이언트 Command q 입력]** <br>
- 클라이언트 프로그램 종료
![image](https://github.com/user-attachments/assets/a6d1f4d0-5ba0-405f-bf9f-8b50d7dff930)
- 클라이언트 프로그램 종료 시 서버 측 출력
![image](https://github.com/user-attachments/assets/2b296c99-27c1-4502-9bf4-3ad1d6de6add)

