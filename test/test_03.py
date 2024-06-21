
import cv2
import math
from ultralytics import YOLO

model = YOLO('yolov8s-pose.pt')
print(model.names)
webcamera = cv2.VideoCapture(0)

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

            # 사람 감지
            height = y2 - y1
            width = x2 - x1
            threshold = height - width

            # 사람 감지
            if conf > 70:
                cv2.putText(frame, f"Total: {len(results[0].boxes)}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            # 쓰러짐 인식
            if threshold < 0:
                cv2.putText(frame, f"Fall Detection", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
            else: pass

    # 프레임 출력
    cv2.imshow("Live Camera", results[0].plot())

    # 나가기 버튼
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 'q' key or 'ESC' key (27)
        break

# 자원 해제
webcamera.release()
cv2.destroyAllWindows()
