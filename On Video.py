from ultralytics import YOLO
import cv2
#Link=https://sghub.deci.ai/models/yolo_nas_pose_s_coco_pose.pth

import os

# 예시 경로
path = 'C:\\Users\\SM-PC\\school\\opensource\\fall_detection_yolov8s-master\\fall_detection_yolov8s-master\\Datasets\\832\\'
files = os.listdir(path)
print("Files in directory:", files)  # 경로에 있는 파일 목록 출력

# 파일 형식 지원 확인
supported_formats = {'jpg', 'jpeg', 'png', 'mp4', 'avi'}
for file in files:
    ext = file.split('.')[-1].lower()
    if ext in supported_formats:
        print(f"Supported file found: {file}")
    else:
        print(f"Unsupported file format: {file}")

# Load a model
model = YOLO('yolov8s-pose.pt',task="pose")  # pretrained YOLOv8n model

# Open the video file
video_path = 'C:\\Users\\SM-PC\\school\\opensource\\fall_detection_yolov8s-master\\fall_detection_yolov8s-master\\Datasets\\832\\video.mp4'  # Replace with the path to your video file
results = model(video_path, stream=True,save=True,device="cpu",imgsz=640)
frame=1
fall=0
for result in results:
    img = result.orig_img
    try:
        boxes = result.boxes  # Boxes object for bbox outputs
        for box in boxes:
            x = boxes.xywh[0][0]
            y = boxes.xywh[0][1]
            w = boxes.xywh[0][2]
            h = boxes.xywh[0][3]
            kpts = result.keypoints
            nk = kpts.shape[1]
            for i in range(nk):
                keypoint = kpts.xy[0, i]
                x, y = int(keypoint[0].item()), int(keypoint[1].item())
                #Draw keypoints on img
                cv2.circle(img, (x, y), 5, (0, 255, 0), -1)  # Draw a green circle at each keypoint location

            if w/h > 1.4:
                fall+=1
                print("Fall detected at {} frame".format(frame))
                
                #Print fall on top of persons head
                cv2.putText(img, "Fallen", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                
            else:
                cv2.putText(img, "Stable", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imwrite("frames/frame_{:04d}.jpg".format(frame), img)  # Use zero-padding with 4 digits
    except:
        pass
    cv2.imwrite("frames/frame_{:04d}.jpg".format(frame), img)  # Use zero-padding with 4 digits
    frame += 1

print("Total fall detected: {}".format(fall))