import math
import os

def create_dir(save_dir, satellite):
        # create /output directory if it does not exist
        if not os.path.isdir("./output"):
            os.makedirs("./output")
            os.chmod("./output", 0o777)

        # create directory inside output if it does not exist, if exists return error
        if os.path.exists(f"{save_dir}"):
            raise ValueError("Directory already exists, please choose a different name.")
        else:
            os.makedirs(f"{save_dir}")
            os.chmod(f"{save_dir}", 0o777)

        if satellite == "sentinel1":
            os.makedirs(f"{save_dir}/sentinel1")
            os.makedirs(f"{save_dir}/sentinel1/tif")
        elif satellite == "sentinel2":
            os.makedirs(f"{save_dir}/sentinel2")
        else:
            os.makedirs(f"{save_dir}/sentinel1")
            os.makedirs(f"{save_dir}/sentinel1/tif")
            os.makedirs(f"{save_dir}/sentinel2")
    
def divide_big_area(coords, step):
        # Create list to hold smaller bounding boxes
        bbox_list = []

        # Calculate the number of tiles (smaller bounding boxes)
        number_boxes_lat = math.ceil(abs(coords[0] - coords[2]) / step) # rows
        number_boxes_lon = math.ceil(abs(coords[1] - coords[3]) / step) # columns

        # Create smaller bounding boxes
        for i in range(number_boxes_lat):
            row_bbox = []
            for j in range(number_boxes_lon):
                bbox = (coords[0] + i * step, coords[1] + j * step, coords[0] + (i + 1) * step, coords[1] + (j + 1) * step)
                row_bbox.append(bbox)
            bbox_list.append(row_bbox)

        return bbox_list

