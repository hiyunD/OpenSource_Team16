import cv2
import cvzone
import math
import time
from ultralytics import YOLO

# 웹캠 설정
webcamera = cv2.VideoCapture(0)

# YOLO 모델 로드
model = YOLO('yolov8s-pose.pt')

# 클래스 이름 로드
classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()

# 사람의 위치와 시간을 저장할 딕셔너리
people_positions = {}

while True:
    ret, frame = webcamera.read()
    frame = cv2.resize(frame, (640, 480))

    results = model(frame)

    current_time = time.time()

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

            if conf > 70 and class_detect == 'person':
                cvzone.cornerRect(frame, [x1, y1, width, height], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=2)

                # Lay Down 감지
                if threshold < 0:
                    cvzone.putTextRect(frame, 'Lay Down', [x1, y1 - 50], thickness=2, scale=2, colorR=(0, 255, 0))

                    # 사람의 현재 위치를 키로 사용하여 위치와 시간을 저장
                    person_id = (x1, y1, x2, y2)
                    if person_id in people_positions:
                        last_position, last_time = people_positions[person_id]
                        if (x1, y1, x2, y2) == last_position:
                            if current_time - last_time >= 2:
                                cvzone.putTextRect(frame, 'Fall Down', [x1, y1 - 100], thickness=2, scale=2, colorR=(0, 0, 255))
                        else:
                            people_positions[person_id] = ((x1, y1, x2, y2), current_time)
                    else:
                        people_positions[person_id] = ((x1, y1, x2, y2), current_time)

    # 지나간 시간을 기반으로 오래된 기록 삭제
    people_positions = {k: v for k, v in people_positions.items() if current_time - v[1] < 2}

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 'q' 키 또는 'ESC' 키 (27)
        break

webcamera.release()
cv2.destroyAllWindows()
