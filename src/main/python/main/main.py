import sys, os, time, ctypes
import cv2
from ultralytics import YOLO


def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True

def shutdown():

    if sys.platform == 'win32':
        user32 = ctypes.WinDLL('user32')
        user32.ExitWindowsEx(0x00000008, 0x00000000)
    else:
        os.system('sudo shutdown now')

def detect(cap, model):
    plastics = 0

    success, frame = cap.read()

    if success:
        results = model.track(frame, persist=True)

        plastics = results[0].boxes.cls.tolist().count(0)
        annotated_frame = results[0].plot()

        x, y, w, h = cv2.getWindowImageRect("Microscope")

        text_size, _ = cv2.getTextSize("Microplastics Detected :"+str(plastics), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        # text_size, _ = cv2.getTextSize("People Detected :"+str(plastics), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_w, text_h = text_size

        cv2.rectangle(annotated_frame, (0,25), ( w, 0-text_h), (0,0,0), -1)
        cv2.putText(annotated_frame, "Microplastics Detected :"+str(plastics), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        # cv2.putText(annotated_frame, "People Detected :"+str(plastics), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        cv2.imshow("Microscope", annotated_frame)

def main():
    global clicked

    # model = YOLO('yolov8n.pt')
    model = YOLO('saltplas.pt')


    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Microscope", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Microscope", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('Microscope', onMouse)

    print('Showing camera feed. Click window or press any key to stop.')

    while cv2.waitKey(1) == -1 and not clicked:
        print(clicked)
        detect(cap, model)

    cv2.destroyAllWindows()
    time.sleep(1)
    shutdown()


if __name__ == "__main__":
    clicked = False
    main()
    