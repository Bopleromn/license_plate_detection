import os
from datetime import datetime
import argparse
import cv2


def save_result(result, filename: str) -> None:
    time = datetime.now()
    time = str(time.year) + '_' +\
        (str(time.month) if len(str(time.month)) == 2 else '0' + str(time.month)) + '_' +\
        (str(time.day) if len(str(time.day)) == 2 else '0' + str(time.day)) + '_' +\
        (str(time.hour) if len(str(time.hour)) == 2 else '0' + str(time.hour)) + '_' +\
        (str(time.minute) if len(str(time.minute)) == 2 else '0' + str(time.minute)) 

    os.makedirs(f'./outputs/{time}')
    result.save(f'./outputs/{time}/{filename}')
    
    
def get_input_filename() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename')

    filename: str = parser.parse_args().filename
    
    if filename is None or filename.find('.') == -1:
        raise Exception('Usage: main.py --filename <filename.ext>')
    
    return filename


def get_region(filename: str, coords):
    x1, y1, x2, y2,  _,  _  = coords
    frame = cv2.imread(filename)
    
    return frame[int(y1):int(y2), int(x1):int(x2)]