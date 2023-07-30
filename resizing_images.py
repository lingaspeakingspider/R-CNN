import cv2 as cv
import os
from pathlib import Path
from typing import Optional

class Resize_Image:

    def __init__(self, image_path: Path, desired_shape:tuple, output_path: Path, output_file_name: Optional[str] = None):
        self.image_path=image_path
        self.desired_shape=desired_shape

        #Resizing
        image=cv.imread(image_path)
        resized_image=cv.resize(image, desired_shape, interpolation=cv.INTER_AREA)

        #Changing to output path and saving
        os.chdir(output_path)
        
        if output_file_name is None:
            file_name=image_path.split("/")
            length=len(file_name)-1
            name=file_name[length]

        else:
            name=output_file_name

        cv.imwrite(name, resized_image)
