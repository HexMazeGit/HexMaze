# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 19:41:17 2021

@author: students
"""

from datetime import datetime, time, timedelta
from decimal import Decimal as D

import pandas as pd
import cv2
import numpy as np
import pytesseract
import random

import matplotlib.pyplot as plt
import seaborn as sns

# change it to argument

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\students\Documents\Hexmaze\video_sync_eye_1\Tesseract-OCR\tesseract.exe'
# %% Function to get median blue and red led intensities


def get_led_intensities(eye, frame):
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

# %% Function to get digits using pytessaract


def get_digits(frame, top, bottom, left, right):
    hsv = cv2.cvtColor(frame[top:bottom, left:right, :], cv2.COLOR_BGR2HSV)
    kernel = np.ones((1, 1), np.uint8)
    hsv = cv2.dilate(hsv, kernel, iterations=1)
    hsv = cv2.erode(hsv, kernel, iterations=1)

    # define range of white color in HSV
    # change it according to your need !
    sensitivity = 50
    lower_white = np.array([0, 0, 255 - sensitivity], dtype=np.uint8)
    upper_white = np.array([255, sensitivity, 255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    result = pytesseract.image_to_string(mask, lang='eng',
                                         config='--psm 9 --oem 1 -c tessedit_char_whitelist=0123456789')

    return result

# %% Get required data from each frame


def get_frame_data(eye, frame):
    # Read integers from frame

    top_num = get_digits(frame, 0, 50, 162, 465)
    bottom_num = get_digits(frame, 40, 100, 140, 420)
    # Get timestamps
    s = top_num.find('2020')
    num_ts = pd.Timestamp(
        datetime(year=int(top_num[s:s + 4]), month=int(top_num[s + 4:s + 6]), day=int(top_num[s + 6:s + 8]),
                 hour=int(top_num[s + 8:s + 10]), minute=int(top_num[s + 10:s + 12]),
                 second=int(top_num[s + 12:s + 14]), microsecond=int(top_num[s + 14:s + 20])))

    # Get top index
    end_ind = top_num.find('\n')
    # bottom_end = bottom_num.find('\n')

    try:
        top_index = int(top_num[s + 20: end_ind])
    except:
        top_index = 0

    try:
        bottom_index = int(bottom_num)
    except:
        bottom_index = 0


# Get the Blue and red  LED intensities
blue_intensity, red_intensity = get_led_intensities(eye, frame)

return num_ts, top_index, bottom_index, blue_intensity, red_intensity

# %% Get eye data

video_loc_eye_1 = r'F:\Hexmaze\maze_videos\eye01_2020-11-09_12-34-18.mp4'
video_loc_eye_2 = r'F:\Hexmaze\maze_videos\eye02_2020-11-09_12-34-18.mp4'
video_loc_eye_3 = r'F:\Hexmaze\maze_videos\eye03_2020-11-09_12-34-18.mp4'
video_loc_eye_4 = r'F:\Hexmaze\maze_videos\eye04_2020-11-09_12-34-18.mp4'
video_loc_eye_5 = r'F:\Hexmaze\maze_videos\eye05_2020-11-09_12-34-18.mp4'
video_loc_eye_6 = r'F:\Hexmaze\maze_videos\eye06_2020-11-09_12-34-18.mp4'
video_loc_eye_7 = r'F:\Hexmaze\maze_videos\eye07_2020-11-09_12-34-18.mp4'
video_loc_eye_8 = r'F:\Hexmaze\maze_videos\eye08_2020-11-09_12-34-18.mp4'
video_loc_eye_9 = r'F:\Hexmaze\maze_videos\eye09_2020-11-09_12-34-18.mp4'
video_loc_eye_10 = r'F:\Hexmaze\maze_videos\eye10_2020-11-09_12-34-18.mp4'
video_loc_eye_11 = r'F:\Hexmaze\maze_videos\eye11_2020-11-09_12-34-18.mp4'
video_loc_eye_12 = r'F:\Hexmaze\maze_videos\eye12_2020-11-09_12-34-18.mp4'

fnames = [video_loc_eye_1, video_loc_eye_2, video_loc_eye_3, video_loc_eye_4, video_loc_eye_5, video_loc_eye_6,
          video_loc_eye_7, video_loc_eye_8, video_loc_eye_9, video_loc_eye_10, video_loc_eye_11, video_loc_eye_12]

# Open a video


# %%  Loop through frames
cap.release()
cap = cv2.VideoCapture(fnames[0])
eye = 1
table = pd.DataFrame(columns=['Frame_number', 'TS', 'Index_top', 'Index_bottom', 'blue_intensity', 'red_intensity'])

while (cap.isOpened()):

    frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    # Read the frame
    res, frame = cap.read()
    if res == True:
        num_ts, top_index, bottom_index, blue_intensity, red_intensity = get_frame_data(eye, frame)

        if frame_index == 0:

            cv2.imshow('Frame 0 ', frame[0:200, 162:500, :])
            cv2.waitKey(5000)
            num_ts_correct = input('Is the ts in the frame ' + str(num_ts) + ' ? Type y or n.')
            if num_ts_correct == 'y':
                pass
            else:
                num = input('Write the digits from 2020 till end of timestamp without space.')
                num_ts = pd.Timestamp(
                    datetime(year=int(num[0:4]), month=int(num[4:6]), day=int(num[6:8]), hour=int(num[8:10]),
                             minute=int(num[10:12]), second=int(num[12:14]), microsecond=int(num[14:20])))
            print('a')

            top_index_correct = input('Is the top index ' + str(top_index) + ' ? Type y or n')
            if top_index_correct == 'y':
                pass
            else:
                top_index = int(input('Write the top index digits without space.'))

            print('b')
            bottom_index_correct = input('Is the bottom index ' + str(bottom_index) + ' ? Type y or n')
            if bottom_index_correct == 'y':
                pass
            else:
                bottom_index = int(input('Write the top index digits without space.'))
            print('c')

        if top_index == 0:
            top_index = table.tail(1)['Index_top'] + 1
        if bottom_index == 0:
            bottom_index = table.tail(1)['Index_bottom'] + 1

        table = table.append({'Frame_number': frame_index,
                              'TS': num_ts,
                              'Index_top': top_index,
                              'Index_bottom': bottom_index,
                              'blue_intensity': blue_intensity,
                              'red_intensity': red_intensity}, True)
    else:
        break



    # %%

    cap.set(cv2.CAP_PROP_POS_FRAMES, 38)
    res, frame = cap.read()
    cv2.imshow('d', frame)
    cv2.waitKey()

    a = get_digits(frame, 40, 100, 170, 420)