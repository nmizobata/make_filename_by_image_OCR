'''
各種画像処理を指定された順序で行う

'''
from pathlib import Path
from typing import Literal
import color_detection as cd

FILTER = Literal["NA",
                 "inverted",
                 "grayscale",
                 "noise_reduction",
                 "high_resolution",
                 "binarization",
                 "red_mask_HSV",
                 "red_masked_HSV",
                 "green_mask_HSV",
                 "green_masked_HSV",
                 "blue_mask_HSV",
                 "blue_masked_HSV",
                 "blue_minus_black_mask_HSV",
                 "blue_minus_black_masked_HSV",
                 "red_mask_RGB",
                 "red_masked_RGB",
                 "green_mask_RGB",
                 "green_masked_RGB",
                 "blue_mask_RGB",
                 "blue_masked_RGB",
                 ]

FILTER_CLASS = Literal[cd.detect_red_color(),
                 cd.detect_green_color(),
                 cd.detect_blue_color()]


class image_filter():
    def __init__(self):
        self.list_filter = ["NA"]
        
    def add_filter(self, filter):
        self.list_fileter.append(filter)
        
    def execute(self, image_path_org:Path):
        import cv2_japanese
        
        image_path = image_path_org
        working_dir = Path(__file__).parent / "image"

        no = 0
        for filter_name in self.list_filter:
            img = cv2_japanese.imread(image_path)
            
            
        