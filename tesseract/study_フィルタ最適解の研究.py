'''
OCRの精度をあげるための手順研究のためのプログラム
/imageに入っているimage.pngをもとに処理を行う。

image.png
'''


from pathlib import Path
import ocr_new
from PIL import Image
import ocr_librarys as lib
import color_detection as cd
import os
import pyocr
import study_imageの取得 as study
import general_library as glib

imagefiles_path = Path(r"D:\FX\★NexT+見立てと振り返り\20250119")
imagefile = "83AUDJPY.png"
image_path = imagefiles_path / imagefile
working_dir = Path(__file__).parent / "image"

if Path(image_path).exists():
    glib.delete_all_file_in_working_dir(Path(__file__).parent / "image")
    # エリア指定
    print("-"*5+" get image and crop")
    area = (8,10,150,44)      # 6枚チャート
    # area = (500,10,635,42)  # 7枚クロスチャート
    # area = (1150, 10, 1270, 42)   # 7枚クロスチャート
    # area = (13,480,100,510)  # EURGBP, Monthly
    # text = ocr_new.get_word_from_cropped_image(chartfile_path,area) 
    image_path = study.get_cropped_imagefile(image_path,area)
    image_path = image_path.rename(image_path.with_name("0_"+image_path.name))
else:
    glib.delete_all_file_in_working_dir(Path(__file__).parent / "image",["0_cropped.png"])
    image_path = working_dir / "0_cropped.png"
    print("-"*5+" use current imagefile {}".format(image_path))


# filtering
number = 0   # フィルタリング順序
print("-"*5+" "+"filterling")
# image_path = lib.make_image_grayscale(image_path)

# image_path = cd.make_image_color_detection("blue_minus_black_mask",image_path)
# image_path = image_path.rename(image_path.with_name("1_"+image_path.name))

# image_path = cd.make_image_color_detection("inverted",image_path)
# image_path = image_path.rename(image_path.with_name("2_"+image_path.name))

# image_path = cd.make_image_color_detection("blue_masked_image",image_path)
# image_path = image_path.rename(image_path.with_name("3_"+image_path.name))

image_path = lib.make_image_noise_reduction(image_path)
image_path = image_path.rename(image_path.with_name("1_"+image_path.name))

# image_path = lib.make_image_high_resolution(image_path)
# image_path = image_path.rename(image_path.with_name("2_"+image_path.name))

# image_path = lib.make_image_grayscale(image_path)
# image_path = image_path.rename(image_path.with_name("3_"+image_path.name))

# image_path = lib.make_image_binary(image_path)
# image_path = image_path.rename(image_path.with_name("4_"+image_path.name))


# image_path = cd.make_image_color_detection("blue_mask",image_path)
print("-"*5+" latest image: {}".format(image_path))

# OCR
print("-"*5+" OCRing")
pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"
tools = pyocr.get_available_tools()
tool = tools[0]

img=Image.open(image_path)
builder = pyocr.builders.TextBuilder(tesseract_layout=6)
text = tool.image_to_string(img,lang="eng",builder=builder)

print("{}: {}".format(image_path.name, text))
