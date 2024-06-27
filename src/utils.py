import os
from datetime import datetime
import argparse
import cv2
import csv
from detection import get_annotated_image

from config import OUTPUT_PATH

def save_result(detection, license_plates_info: list, filename: str) -> None:
    time = datetime.now()
    time = str(time.year) + '_' +\
        (str(time.month) if len(str(time.month)) == 2 else '0' + str(time.month)) + '_' +\
        (str(time.day) if len(str(time.day)) == 2 else '0' + str(time.day)) + '_' +\
        (str(time.hour) if len(str(time.hour)) == 2 else '0' + str(time.hour)) + '_' +\
        (str(time.minute) if len(str(time.minute)) == 2 else '0' + str(time.minute))  + '_' +\
        (str(time.second) if len(str(time.second)) == 2 else '0' + str(time.second)) 

    dirname = OUTPUT_PATH + time

    os.makedirs(dirname)
    
    filename = filename[filename.rfind(os.sep) + 1:]
    
    # save image
    cv2.imwrite(os.path.join(dirname, filename), get_annotated_image(filename))
    # detection.save(os.path.join(dirname, filename))
    
    # save csv
    with open(os.path.join(dirname, f'{filename[:filename.find(".")]}.csv'), mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=license_plates_info[0].keys())
        
        writer.writeheader()
        writer.writerows(license_plates_info)
    
    
def get_input_filename() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename')

    filename: str = parser.parse_args().filename
    
    if filename is None or filename.find('.') == -1:
        raise Exception('Usage: main.py --filename <filename.ext>')
    
    return filename


def get_region(frame: str, coords, is_video=False):
    x1, y1, x2, y2,  _,  _  = coords
    if not is_video:
        frame = cv2.imread(frame)
    
    return frame[int(y1):int(y2), int(x1):int(x2)]