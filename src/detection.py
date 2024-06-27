from ultralytics import YOLO
import easyocr
import re
import cv2

from utils import get_region
from config import CAR_MODEL_PATH, PLATE_MODEL_PATH


car_detector = YOLO(CAR_MODEL_PATH)
plate_detector = YOLO(PLATE_MODEL_PATH)


def track_cars(frame) -> list:
    car_coords = []
    # make default YOLO model find cars
    cars = car_detector(frame)[0]
    
    # iterate over coordinates(x1, y1, x2, y2) and save them
    for vehicle in cars.boxes.data.tolist():
        x1, y1, x2, y2, _, _ = vehicle
        car_coords.append([x1, y1, x2, y2])
        
    return car_coords


def get_car(license_plate, cars_coords) -> tuple:
    x1, y1, x2, y2, _, _  = license_plate
    for car_coord in cars_coords:
        x1_car, y1_car, x2_car, y2_car = car_coord
        if x1 > x1_car and x2 < x2_car and y1 > y1_car and y2 < y2_car:
            return (True, car_coord)
        
    return (False, [-1, -1, -1, -1])

                
def track_license_plates(frame, cars_coords: list, is_video=False) -> list:
    license_plates_info = []
    
    license_plates = plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
       success, car_coords = get_car(license_plate, cars_coords)
       x1, y1, x2, y2, _, _ = license_plate
       x1_car, y1_car, x2_car, y2_car  = car_coords
       if success:
            text = get_text_from_license_plate(frame, license_plate, is_video=is_video)
            license_plates_info.append({
                'x1_car': int(x1_car), 'y1_car': int(y1_car), 'x2_car': int(x2_car), 'y2_car': int(y2_car), 
                'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2),
                'text': text
            })
            
    return license_plates_info


def get_text_from_license_plate(frame, license_plate, is_video=False) -> str:
    reader = easyocr.Reader(['en'], gpu=False)
    
    frame = get_region(frame, license_plate, is_video=is_video)
    strs = [] 
    
    img = cv2.imread(frame)
    
    for detection in reader.readtext(frame):
        top_left = [int(value) for value in detection[0][0]]
        bottom_right = [int(value) for value in detection[0][2]]
        text = detection[1]
        
        img = cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 5)
        img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
        
        reg = re.compile('[^A-Za-z0-9]')
        strs.append(reg.sub('', text))
        
    return ''.join(strs)


def get_annotated_image(frame):
    reader = easyocr.Reader(['en'], gpu=False)
    
    img = cv2.imread(frame)
    
    for detection in reader.readtext(frame):
        top_left = [int(value) for value in detection[0][0]]
        bottom_right = [int(value) for value in detection[0][2]]
        text = detection[1]
        
        img = cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 5)
        img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)    
    
    return img


def get_license_detections(frame):
    return plate_detector(frame)[0]