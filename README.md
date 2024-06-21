# <OpenSource_Team16><br/>
YOLO POSE 기반 독거노인 쓰러짐 발견 및 알림 소프트웨어
<br/>

### <<파일 실행 전 yolov8s-pose.pt 설치>> 

### test_05(sample).py
> test_03.py 배경으로 제작

> 파일 내 수정 필요
> > email_user = '경고 메시지 보낼 이메일 계정'<br/>
> > email_password = '보낼 계정의 비밀번호'<br/>
> > recipient_email = '경고 메시지 받을 이메일 계정'

> 이메일 사이트 > 보안 > 보안 수준이 낮은 앱의 액세스 허용

### test_03.py
> interface는 app.py이고 기능은 test_02.py의 fall detection으로 가져와 합침<br/>
> classes.txt 설치 필요 없음<br/>

### test_02.py
> https://www.youtube.com/watch?v=wrhfMF4uqj8<br/>
> 위 영상 기반으로 제작

> 웹캠으로 인식하도록 수정함<br/>
> pip install cvzone 해야함<br/>
> classes.txt 설치 필수<br/>

### On Video.py
> 실행하려면 경로 재설정 해야함<br/>
> 비디오에 프레임을 씌워서 새로 비디오를 생성<br/>
