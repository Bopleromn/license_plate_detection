from ultralytics import YOLO
import easyocr
import re

from utils import get_region


car_detector = YOLO('./models/yolov8n.pt')
plate_detector = YOLO('./models/license_plate_detector.pt')


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

                
def track_license_plates(frame, cars_coords: list) -> list:
    license_plates_info = []
    
    license_plates = plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
       success, car_coords = get_car(license_plate, cars_coords)
       x1, y1, x2, y2, _, _ = license_plate
       x1_car, y1_car, x2_car, y2_car  = car_coords
       if success:
            text = get_text_from_license_plate(frame, license_plate)
            license_plates_info.append({
                'car': {'coords': [int(x1_car), int(y1_car), int(x2_car), int(y2_car)]},
                'license_plate': {
                    'coords': [int(x1), int(y1), int(x2), int(y2)],
                    'text': text
                }
            })
            
    print(license_plates_info)
       
    return license_plates_info


def get_text_from_license_plate(frame, license_plate) -> str:
    reader = easyocr.Reader(['en'], gpu=False)
    
    frame = get_region(frame, license_plate)
    strs = [] 
    
    for detection in reader.readtext(frame):
        _, text, _ = detection
        
        reg = re.compile('[^A-Za-z0-9]')
        strs.append(reg.sub('', text))
        
    return ''.join(strs)