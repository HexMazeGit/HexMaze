"""
File that allows the generation and save of the data

Created on Oct 2021

@author: Mutu
         Juan
"""

import glob # Library to manage Files Names
import Functions as f

# Route containing all the videos
str_Route = r'D:\Hexmaze\maze_videos\*.mp4'
fileslist = glob.glob(str_Route) # Get all files in the path
fileslist.pop() # Remove last file of the list (stitched.mp4)
str_SaveRoute = r'D:\Hexmaze\maze_videos\CSV_'
for file in fileslist:
    str_SaveName = str_SaveRoute + file[23:-4] + '.csv' # Save a file with same name but different extention (CSV)
    f.f_Get_TimeStamps (file,str_SaveName)

# Validation of the Detection
str_SaveRoute = r'D:\Hexmaze\maze_videos\CSV_'
fileslist = glob.glob(str_SaveRoute) # Get all files in the path
fileslist.pop() # Remove last file of the list (stitched.mp4)
# TODO: For validation: cycle for video and text documents
# TODO: For Validation: Plot segment and the corresponding text
# Todo: For Validation: Get user input (input function*)



