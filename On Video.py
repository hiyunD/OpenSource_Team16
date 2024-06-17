from ultralytics import YOLO
import cv2
import os

# # 예시 경로
# path = 'C:\\Users\\SM-PC\\school\\opensource\\fall_detection_yolov8s-master\\Datasets\\832\\'
# files = os.listdir(path)
# print("Files in directory:", files)

# # 파일 형식 지원 확인
# supported_formats = {'mp4', 'avi'}
# for file in files:
#     ext = file.split('.')[-1].lower()
#     if ext in supported_formats:
#         print(f"Supported file found: {file}")
#     else:
#         print(f"Unsupported file format: {file}")

# Load a model
model = YOLO('yolov8s-pose.pt', task="pose")

# Open the video file
video_path = 'C:\\Users\\SM-PC\\school\\opensource\\final\\fall_detection_yolov8s-master\\Datasets\\832\\video.mp4'
results = model(video_path, stream=True, save=True, device="cpu", imgsz=640)
frame = 1
fall = 0
for result in results:
    try:
        boxes = result.boxes
        for box in boxes:
            w = boxes.xywh[0][2]
            h = boxes.xywh[0][3]
            if w/h > 1.4:
                fall += 1
                print("Fall detected at frame {}".format(frame))
            else:
                print("Stable at frame {}".format(frame))
    except:
        pass
    frame += 1

print("Total fall detected: {}".format(fall))
