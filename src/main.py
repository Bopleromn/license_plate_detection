import cv2

from utils import get_input_filename
from detection import track_cars, track_license_plates


def main() -> None:
    filename = get_input_filename()
    ext = filename[filename.find('.'):]

    if ext in ['.jpg', '.jpeg', '.png']:
        # track vehicles
        car_coords = track_cars(filename)
        
        # get license plate info
        license_plates_info = track_license_plates(filename, car_coords)

        # TODO: save data(image with detected license and text, and csv file)
    elif ext in ['.mp4']: 
        cap = cv2.VideoCapture('./sample.mp4')
        frame_num = -1
        is_running = True
        while is_running:
            frame_num += 1
            is_running, frame = cap.read()
            car_coords = track_cars(filename)
            license_plates_info = track_license_plates(filename, car_coords)

        

    else:
        raise Exception('Unsupported file format')
    
main()