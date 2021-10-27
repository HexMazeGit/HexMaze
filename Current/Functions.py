"""
Folder containing all the functions related to Hexmaze video syncronization
Created on Oct 2021

@author: Mutu
         Juan
"""

## Import libraries
import cv2 # Image processing libray
import pandas as pd
import numpy as np
import pytesseract # Library for Image to text convertion
# Setup pytesseract
from datetime import datetime, time, timedelta  # Library for Time objects
pytesseract.tesseract_cmd = r'D:\Hexmaze\video_sync_eye_1\Tesseract-OCR\tesseract.exe'
import csv # Library to write the data in csv file


## Fucntion to get all index in a given video
def f_Get_TimeStamps (str_videoName,str_SaveName):
    """
    Create a CSV File containing the information of of the timestamps, frame index and intensity of the leds
    :param str_videoName: Name of the video to be processed
    :param str_SaveName: Name of the CSV to be created
    :return: NA
    """
    s_Eye = int(str_videoName[26:28]) # Get Eye number
    cap.release()
    cap = cv2.VideoCapture(str_videoName) # Initialize video for reading
    s_Number_of_Frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Initialize File to store data
    csv_File = open(str_SaveName, 'w')
    writer = csv.writer(csv_File)
    Header = ['Frame_number','Time_Stamp','Current_Index','Previous_Index','Blue_Intensity','Red_Intensity']
    writer.writerow(Header)
    # Check everye frame in video
    cont = 0
    while (cap.isOpened()):
        frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) # Current Frame Index
        res, frame = cap.read() # Read Current Frame
        # Validate for First Index
        # NOTE: It is only necesary to get the frame number on the first frame because they have one unit increment.
        if frame_index <= 1:
            # Cut the  frames
            v_Index_CurrFrame = [56, 71, 267, 331]  # Index containing the data for the current frame
            Curr_Frame_Index = f_CutFrame(frame, v_Index_CurrFrame)
            str_CurrFrame = f_GetFrameNum(Curr_Frame_Index)

            v_Index_PrevFrame = [19, 34, 380, 466]  # Index containing the date for the previpus frame
            Prev_Frame_Index = f_CutFrame(frame, v_Index_PrevFrame)
            str_PrevFrame = f_GetFrameNum(Prev_Frame_Index)
        else:
            str_CurrFrame += 1
            str_PrevFrame += 1

        v_IndexTime = [19, 34, 175, 380]  # Index for the time Stamp
        Prev_Frame_Times = f_CutFrame(frame, v_IndexTime)
        top_num = f_GetFrameNum(Prev_Frame_Times)
        s = 0 # Define Starting Point
        num_ts = pd.Timestamp(
            datetime(year=int(top_num[s:s + 4]), month=int(top_num[s + 4:s + 6]), day=int(top_num[s + 6:s + 8]),
                     hour=int(top_num[s + 8:s + 10]), minute=int(top_num[s + 10:s + 12]),
                     second=int(top_num[s + 12:s + 14]), microsecond=int(top_num[s + 14:s + 20])))
        str_TimeStamp = str(num_ts)

        # TODO: Ask Mutu about Median intensity function ...
        blue_intensity, red_intensity = get_led_intensities(cap, frame)
        # Prepare Data in string to write
        row = [str(frame_index),str_TimeStamp,str_CurrFrame,str_PrevFrame,str(blue_intensity),str(red_intensity)]
        # Print in File
        writer.writerow(row)
    csv_File.close()



def f_CutFrame(frame, Index):
    """
    Cut the given frame accordin to the index
    Parameters
    ----------
    frame : Frame
        The current Frame to be cut matriz expected.
    Index : vector
        Vector containing the index to cut the matrix, 4 index are expected

    Returns
    -------
        m_cut: Image
    Segment of the original frame cutted acording to the index.

    """
    m_Cut = frame[Index[0]:Index[1], Index[2]:Index[3]]
    return m_Cut


## Attepmt to get Diggits
def f_GetFrameNum(Image):
    """
    Fiction to binarize the image and get the corresponding diggits

    :param Image:  Image to get the numbers from
    :return: Digitst found using the algorithm
    """
    # Get black and white image
    sensitivity = 50
    # Define limits for binarizarion
    lower_white = np.array([0, 0, 255 - sensitivity], dtype=np.uint8)
    upper_white = np.array([255, sensitivity, 255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(Image, lower_white, upper_white)

    # Convert mask to digits (Credit to MUTU just coppied her config)
    str_Dig = pytesseract.image_to_string(mask, lang='eng', config='--psm 9 --oem 1 -c tessedit_char_whitelist=0123456789')
    return str_Dig

def get_led_intensities(eye, frame):
    """

    :param eye: Index of the Video?
    :param frame: Image of the frame been evaluated
    :return:
    mean intensity of both leds in the video.
    """
    eye = eye - 1


# Blue led regions
b_left = [730, 730, 728, 723, 620, 0, 626, 631, 647, 650, 721, 722]
b_right = [735, 735, 732, 728, 623, 0, 631, 635, 651, 655, 725, 725]
b_top = [562, 189, 477, 114, 380, 0, 24, 394, 117, 488, 230, 568]
b_bottom = [566, 195, 481, 118, 384, 0, 28, 398, 120, 492, 235, 572]

# Red led regions
r_left = [730, 729, 728, 723, 625, 606, 627, 632, 648, 650, 717, 718]
r_right = [733, 734, 733, 727, 627, 609, 631, 635, 652, 655, 720, 721]
r_top = [569, 194, 483, 119, 384, 40, 20, 389, 112, 483, 227, 565]
r_bottom = [572, 198, 487, 122, 387, 43, 23, 393, 115, 488, 232, 568]

# Preprocess frame and crop led regions
frame_p = cv2.equalizeHist(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
blue_region = frame_p[b_left[eye]:b_right[eye], b_top[eye]:b_bottom[eye]]
red_region = frame_p[r_left[eye]:r_right[eye], r_top[eye]:r_bottom[eye]]

# Get median values
blue_median = np.median(cv2.resize(blue_region, (75, 75)))
red_median = np.median(cv2.resize(red_region, (75, 75)))

return blue_median, red_median