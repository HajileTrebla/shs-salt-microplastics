import sys, os, time, ctypes
import RPi.GPIO as GPIO
from datetime import date, datetime
from os.path import dirname, join
import cv2
from ultralytics import YOLO


def init_setup():
    global root_path
    os.makedirs(os.path.join(root_path, 'saved_images'), exist_ok=True)

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

def capture(data):
    global root_path

    save_dir = os.path.join(root_path, 'saved_images')

    frame, count, text_w, text_h = data
    path_time = datetime.now().strftime("%d%m%y.%H%M%S")

    file_name = os.path.join(save_dir,str(path_time)+'.jpeg')

    cv2.rectangle(frame, (0,65), ( text_w, 0-(text_h*2)), (0,0,0), -1)
    cv2.putText(frame, "Microplastics Detected :"+str(count), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    cv2.putText(frame, "Time :"+str(datetime.now().strftime("%d/%m/%y %H:%M:%S")), (20,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

    cv2.imwrite(file_name, frame)
    print('Captured Image : {}'.format(file_name))

def stream(cap, model):
    plastics = 0

    success, frame = cap.read()

    if success:
        results = model.track(frame, persist=True)

        plastics = results[0].boxes.cls.tolist().count(0)
        annotated_frame = results[0].plot()

        x, y, w, h = cv2.getWindowImageRect("Microscope")

        text_size, _ = cv2.getTextSize("Microplastics Detected :"+str(plastics), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_w, text_h = text_size

        cv2.rectangle(annotated_frame, (0,25), ( w, 0-(text_h*2)), (0,0,0), -1)
        cv2.putText(annotated_frame, "Microplastics Detected :"+str(plastics), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        cv2.imshow("Microscope", annotated_frame)
    return annotated_frame, plastics, w, text_h

def detect():
    global clicked
    global root_path
    global btn

    model_path = join(root_path, 'saltplas.pt')

    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Microscope", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty("Microscope", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('Microscope', onMouse)

    print('Showing camera feed. Click window or press any key to stop.')

    while GPIO.input(btn):
        while cv2.waitKey(1) == -1 and not clicked:
            if not GPIO.input(btn):
                break
            stream(cap, model)
        capture(stream(cap, model))
        clicked = False

    cv2.destroyAllWindows()
    time.sleep(1)

    GPIO.cleanup()
    print('shutdown')
    # shutdown()

def buttonSet():
    global btn

    btn = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
    global clicked
    global root_path

    root_path = dirname(dirname(dirname(dirname(dirname(__file__)))))
    clicked = False

    buttonSet()

    init_setup()
    detect()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)