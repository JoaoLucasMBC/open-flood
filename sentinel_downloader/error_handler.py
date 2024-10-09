import sys
import os
from datetime import datetime

def satellite_error_handling(satellite: str):
    if not isinstance(satellite, str):
        raise ValueError("Invalid satellite, please input a string.")
    if satellite not in ["sentinel1", "sentinel2", "sen1", "sen2", "s1", "s2"]:
        raise ValueError("Invalid satellite, please choose between 'sentinel1/sen1/s1' or 'sentinel2/sen2/s1'.")
    if satellite in ["sen1", "s1"]:
        return "sentinel1"
    if satellite in ["sen2", "s2"]:
        return "sentinel2"
    return satellite

def coordinate_error_handling(coords: tuple):
    if not isinstance(coords, tuple):
        raise ValueError("Invalid coordinates, please input a tuple.")
    if len(coords) != 4:
        raise ValueError('Invalid coordinates, please input 4 values for the north-west latitude, north-west longitude, south-east latitude, and south-east longitude, respectively.')
    if not all(isinstance(coord, (int, float)) for coord in coords):
        raise ValueError("Invalid coordinates, all tuple values must be integers or floats.")
    if coords[0] < coords[2]:
        raise ValueError("Invalid coordinates, the latitude of the northwest corner must be greater than the latitude of the southeast corner.")
    if not (-90 <= coords[0] <= 90 and -180 <= coords[1] <= 180 and -90 <= coords[2] <= 90 and -180 <= coords[3] <= 180):
        raise ValueError("Invalid coordinates, latitude value must be between -90 and 90 and longitude value must be between -180 and 180.")

def time_interval_error_handling(time_interval: tuple):
    if not isinstance(time_interval, tuple):
        raise ValueError("Invalid time interval, please input a tuple.")
    if len(time_interval) != 2:
        raise ValueError("Invalid time interval, please input 2 values for the start and end date, respectively.")
    if not all(isinstance(date, str) for date in time_interval):
        raise ValueError("Invalid time interval, both values must be strings.")
    try:
        time_interval = (datetime.strptime(time_interval[0], "%Y-%m-%d"), datetime.strptime(time_interval[1], "%Y-%m-%d"))
    except:
        raise ValueError("Invalid date format, it must be in the format 'YYYY-MM-DD'.")
    if time_interval[0] > time_interval[1]:
        raise ValueError("Invalid time interval, the first date must be before the second date.")
    if time_interval[0] < datetime.strptime("2015-07-01", "%Y-%m-%d"):
        raise ValueError("Invalid time interval, the start date must be after 2015-07-01 (Sentinel 1 and Sentinel 2 data availability).")
    if time_interval[1] > datetime.now():
        raise ValueError("Invalid time interval, the end date must be before the current date.")
    if time_interval[0] > datetime.now():
        raise ValueError("Invalid time interval, the start date must be before the current date.")
    
def resolution_error_handling(resolution: int, satellite: str):
    if not isinstance(resolution, int):
        raise ValueError("Invalid resolution, please input an integer.")
    if resolution <= 0:
        raise ValueError("Invalid resolution, it must be greater than 0.")
    if satellite == "sentinel1":
        if resolution not in [128,256,512]:
            raise ValueError("Invalid resolution, please choose between 128, 256, or 512 for Sentinel 1.")
    if satellite == "sentinel2":
        if resolution not in [128,256,512,1024,2048]:
            raise ValueError("Invalid resolution, please choose between 128, 256, 512, 1024, or 2048 for Sentinel 2.")
    
def save_dir_error_handling(save_dir: str):
    if not isinstance(save_dir, str):
        raise ValueError("Invalid save directory, please input a string.")
    full_dir = f"/output/{save_dir}"
    if os.path.exists(full_dir):
        raise ValueError("Invalid save directory, a folder with the same name already exists.")
    
def filename_error_handling(filename: str):
    if not isinstance(filename, str):
        raise ValueError("Invalid filename, please input a string.")
    if "/" in filename or "\\" in filename or "." in filename or " " in filename:
        raise ValueError("Invalid filename, it must not contain any special characters, spaces, or file extensions.")