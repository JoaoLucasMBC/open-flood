from sentinel_downloader.sentinel1 import Sentinel1
from sentinel_downloader.sentinel2 import Sentinel2
from sentinel_downloader.utils import create_dir, divide_big_area, load_evalscript
from sentinel_downloader.error_handler import *
from sentinel_downloader.image_processing import process_image, normalize, png_conversion
import ast
from datetime import datetime
import shutil
import json

class JSONRunner():

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    
    def load_config(self):
        with open(self.config_file) as f:
            return json.load(f)
    
    def run(self):
        if "satellite" not in self.config:
            raise ValueError("No satellite specified, please input a satellite (sentinel1, sentinel2, or both).")
        if "coords" not in self.config:
            raise ValueError("No coordinates specified, please input coordinates.")
        if "time_interval" not in self.config:
            raise ValueError("No time interval specified, please input a time interval.")
        
        satellite = self.config["satellite"]
        coords = self.config["coords"]
        time_interval = self.config["time_interval"]
        resolution = self.config["resolution"] if "resolution" in self.config else 512
        save_dir = self.config["save_dir"] if "save_dir" in self.config else f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        filename = self.config["filename"] if "filename" in self.config else "file"
        evalscript = self.config["evalscript"] if "evalscript" in self.config else "rgb"
        cloud_removal = self.config["cloud_removal"] if "cloud_removal" in self.config else False
        
        save_dir_created = False

        try:
            # Error handling

            # Check if satellite is valid
            satellite = satellite_error_handling(satellite)

            coords = ast.literal_eval(coords)
            coordinate_error_handling(coords)
            coords = (coords[1], coords[0], coords[3], coords[2])
            

            time_interval = ast.literal_eval(time_interval)
            time_interval_error_handling(time_interval)


            resolution_error_handling(resolution, satellite)
            resolution = (resolution, resolution)
            step = 0.0459937425 * resolution[0] / 512

            save_dir_error_handling(save_dir)
            save_dir = os.path.join(os.getcwd(), "output", save_dir)
            create_dir(save_dir, satellite)
            save_dir_created = True

            filename_error_handling(filename)

            if satellite == "sentinel2" or satellite == "both":
                
                evalscript_error_handling(evalscript)
                evalscript = load_evalscript(evalscript)

                cloud_removal_error_handling(cloud_removal)

                sentinel2 = Sentinel2()

                if abs(abs(coords[0]) - abs(coords[2])) > step or abs(abs(coords[1]) - abs(coords[3])) > step:
                    list_coords = divide_big_area(coords, step)
                else:
                    list_coords = [[coords]]
                
                if cloud_removal:
                    sentinel2.collect_best_image(list_coords, evalscript, time_interval, resolution, save_dir, filename)
                else:
                    sentinel2.collect_image(list_coords, evalscript, time_interval, resolution, save_dir, filename)

            if satellite == "sentinel1" or satellite == "both":

                sentinel1 = Sentinel1()

                if abs(abs(coords[0]) - abs(coords[2])) > step or abs(abs(coords[1]) - abs(coords[3])) > step:
                    list_coords = divide_big_area(coords, step)
                else:
                    list_coords = [[coords]]

                sentinel1.collect_image(list_coords, coords, time_interval, save_dir, filename)

                vv_vh_list, filenames = process_image(save_dir)

                image_final_list = normalize(vv_vh_list)
                png_conversion(image_final_list, filenames, save_dir, resolution[0])
                
        except Exception as e:
            if save_dir_created:
                shutil.rmtree(save_dir)
            print(e)

if __name__ == "__main__":
    runner = JSONRunner("config.json")
    runner.run()