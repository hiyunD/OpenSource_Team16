import cv2
import math
import time
from ultralytics import YOLO

# GUI
import tkinter as tk
from tkinter import messagebox

import smtplib
from email.mime.text import MIMEText


# 이메일 설정
smtp_server = 'smtp.naver.com'
smtp_port = 587
email_user = '경고 메시지 보낼 이메일 계정'
email_password = '보낼 계정의 비밀번호'
recipient_email = '경고 메시지 받을 이메일 계정'

# gmail 보내는 함수
def send_email():
    subject = "넘어짐이 감지되었습니다."
    body = "피보호자의 응급상황입니다."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 경고 창 띄우기 함수
def show_warning():
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨김
    messagebox.showwarning("Warning", 
                           "5초 이상 쓰러짐이 감지되었습니다.\n기능에 저장된 보호자와 응급시설에 연락을 보냅니다.")
    root.destroy()

model = YOLO('yolov8s-pose.pt')
print(model.names)
webcamera = cv2.VideoCapture(0)

# 쓰러짐이 처음 감지된 시간을 저장하는 변수
fall_start_time = None 

while True:
    # 웹캠 프레임 읽기
    success, frame = webcamera.read()
    
    # 모델 사용하여 객체 감지
    results = model.track(frame, classes=0, conf=0.8, imgsz=480)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            conf = math.ceil(confidence * 100)

            # 사람 감지 수식
            height = y2 - y1
            width = x2 - x1
            threshold = height - width

            # 사람 감지
            if conf > 70:
                cv2.putText(frame, f"People: {len(results[0].boxes)}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            # 쓰러짐 인식
            if threshold < 0:
                cv2.putText(frame, f"Fall Detection", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                if fall_start_time is None:
                    fall_start_time = time.time()
                elif time.time() - fall_start_time >= 5:
                    send_email()
                    show_warning()
                    fall_start_time = None  # 경고를 한번 띄운 후 초기화

            else:
                fall_start_time = None  # 쓰러짐이 아닌 상태로 돌아오면 초기화

    # 프레임 출력
    cv2.imshow("Live Camera", results[0].plot())

    # 나가기 버튼
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 'q' key or 'ESC' key (27)
        break

# 자원 해제
webcamera.release()
cv2.destroyAllWindows()
