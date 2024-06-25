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
        # TODO: do the same but with video and output video with detected plates and text
        pass
    else:
        raise Exception('Unsupported file format')
    
main()