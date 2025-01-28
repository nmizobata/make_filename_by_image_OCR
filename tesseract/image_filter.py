'''
各種画像処理を指定された順序で行う

'''
from pathlib import Path

class ImageFilter:
    def __init__(self):
        self.list_filter = []
        
    def add(self, filter):
        self.list_filter.append(filter)
    
    def __str__(self):
        return "image_filters: {}".format(self.list_filter)
        
    def execute(self, image_path_org:Path, display:bool=False)->Path:
        image_path = image_path_org
        for enum, filter in enumerate(self.list_filter, start=1):
            filter.set_image_path(image_path)
            filter.set_serial_number(enum)
            if display:
                print(" filter{}: {}".format(enum, filter))
            image_path = filter.execute()
        return image_path
            
        