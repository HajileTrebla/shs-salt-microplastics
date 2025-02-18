import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
# model = YOLO('yolov8n.pt')
model = YOLO('saltplas.pt')

# Open the video file
cap = cv2.VideoCapture(0)
plastics = 0

# Loop through the video frames
while cap.isOpened():

    success, frame = cap.read()

    if success:
        results = model.track(frame, persist=True)

        plastics = results[0].boxes.cls.tolist().count(0)
            
        annotated_frame = results[0].plot()

        cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        x, y, w, h = cv2.getWindowImageRect("Webcam")

        text_size, _ = cv2.getTextSize("Microplastics Detected :"+str(plastics), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        # text_size, _ = cv2.getTextSize("People Detected :"+str(plastics), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_w, text_h = text_size

        cv2.rectangle(annotated_frame, (0,25), ( w, 0-text_h), (0,0,0), -1)
        cv2.putText(annotated_frame, "Microplastics Detected :"+str(plastics), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        # cv2.putText(annotated_frame, "People Detected :"+str(plastics), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        
        cv2.imshow("Webcam", annotated_frame)

        if cv2.waitKey(1) == ord('q'):
            break