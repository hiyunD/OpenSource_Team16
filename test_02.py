import cv2
import cvzone
import math
from ultralytics import YOLO
import time
import tkinter as tk
from tkinter import messagebox


# cap = cv2.VideoCapture('video.mp4')
webcamera = cv2.VideoCapture(0)

model = YOLO('yolov8s-pose.pt')

def show_alert():
    # 알림창 띄우기 (Tkinter 팝업)
    messagebox.showwarning("알림", "넘어짐이 감지되었습니다!")

def alert():
    # 별도의 스레드에서 알림창과 소리 재생
    alert_thread = threading.Thread(target=show_alert)
    alert_thread.start()

classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()

while True:
    # ret, frame = cap.read()
    ret, frame = webcamera.read()
    frame = cv2.resize(frame, (640, 480))

    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            height = y2 - y1
            width = x2 - x1
            threshold = height - width
            start_time = None

            if conf > 70 and class_detect == 'person':
                cvzone.cornerRect(frame, [x1, y1, width, height], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=1, scale=1)

            if threshold < 0:
                cvzone.putTextRect(frame, 'fall detection', [height, width], thickness=1, scale=1)
                if start_time is None:
                    # 조건이 처음 만족되는 시점의 시간을 기록
                    start_time = time.time()
                elif time.time() - start_time >= 5:
                    alert()
                    print("쓰러졌습니다....")
                else:
                    start_time = None
            else:pass
            time.sleep(0.1)

        
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 'q' key or 'ESC' key (27)
        break

# cap.release()
webcamera.release()
cv2.destroyAllWindows()