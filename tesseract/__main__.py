import os
from pathlib import Path
from pdf2image import convert_from_path

basepath = r"C:\Users\blues\OneDrive\ドキュメント\Python Projects\make_filename_by_image_OCR\tesseract"
# poppler_dir = Path(__file__).parent.absolute() / "poppler/Library/bin"
poppler_dir = basepath + "/poppler/Library/bin"

os.environ["PATH"] += os.pathsep + str(poppler_dir)
# todo: os.environコマンドは、プログラム実行がおわるとどうなるのか確認する

# pdf_path = Path(__file__).parent.absolute() / "/pdf/sample.pdf"
# img_path = Path(__file__).parent.absolute() / "/image"

pdf_path = basepath + "/pdf/sample.pdf"
img_path = basepath + "/image"

# convert_from_path(pdf_path, output_folder=img_path, fmt='png',output_file=pdf_path.stem)
convert_from_path(pdf_path,output_folder=img_path, fmt='png',output_file="sample")

# todo: pathlibのPathの動作を確認する。stem?
# todo: convert_from_pathの引数の使い方を確認する。
# 
