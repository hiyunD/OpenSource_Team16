import cv2
import numpy as np
from ultralytics import YOLO
import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading

# YOLOv8 모델 로드
model = YOLO('yolov8s-pose.pt')  # 적절한 모델 파일로 변경 필요

# Tkinter 초기화
root = tk.Tk()
root.withdraw()  # Tkinter 창 숨기기

def detect_fall(keypoints):
    """
    넘어지는 상황을 감지하는 함수
    간단한 예로, 어깨와 엉덩이의 y 좌표를 비교하여 넘어짐을 감지합니다.
    """
    left_shoulder_y = keypoints[5][1]
    right_shoulder_y = keypoints[6][1]
    left_hip_y = keypoints[11][1]
    right_hip_y = keypoints[12][1]

    # 어깨가 엉덩이보다 현저히 낮은 경우 넘어짐으로 간주
    if (left_shoulder_y > left_hip_y + 50) and (right_shoulder_y > right_hip_y + 50):
        return True
    return False

def show_alert():
    # 알림창 띄우기 (Tkinter 팝업)
    messagebox.showwarning("알림", "넘어짐이 감지되었습니다!")
    # 소리 재생
    playsound('alert_sound.mp3')  # 경고음 파일 경로로 변경

def alert():
    # 별도의 스레드에서 알림창과 소리 재생
    alert_thread = threading.Thread(target=show_alert)
    alert_thread.start()

# 비디오 캡처 객체 생성 (웹캠 사용)
cap = cv2.VideoCapture(0)

fall_detected = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv8로 사람 감지 및 포즈 추정
    results = model.track(frame, classes=0, conf=0.8, imgsz=480)
    cv2.putText(frame, f"인원: {len(results[0].boxes)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    

    # 결과 객체의 구조를 확인하고 올바른 인덱싱 적용
    for result in results:
        try:
            print(result)  # 결과 객체의 구조 확인
        except IndexError as e:
            print(f"IndexError: {e}")

        if isinstance(result, dict) and 'class' in result:
            if result['class'] == 0:  # 사람이 감지된 경우
                keypoints = result['keypoints']
                if detect_fall(keypoints):
                    if not fall_detected:
                        fall_detected = True
                        alert()  # 알림창 띄우기 및 소리 재생
                else:
                    fall_detected = False

    # 결과 영상 출력
    cv2.imshow("", results[0].plot())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
