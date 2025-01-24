'''
イメージのエリアを指定してイメージを切り出し、ワードとして読み取る。
イメージは/tesseract/imageに保存する。
切り出したイメージはimageフォルダの中にcropped.pngとして保存される。
ocrは自作ライブラリ。
20250124 K1.0 
'''

import ocr
from pathlib import Path

basepath = Path(__file__).parent
# image_filename = "01EURクロス.png"
image_filename = "71EURCHF.png"
print(basepath / "image" / image_filename)

area = (10,10,150,40)
# area = (500,10,630,40)
# area = (510, 490, 625, 515)
# area = (1150, 10, 1270, 40)

text = ocr.get_word_from_image(basepath / "image" / image_filename, area)
print(text)