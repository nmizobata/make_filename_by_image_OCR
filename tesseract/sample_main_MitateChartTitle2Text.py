'''
日々の見立てチャートファイルのファイル名自動変換
EUR等のクロスチャートやGBPAUD等のマルチタイムチャートの画像ファイルのファイル名を自動付加する

'''
from pathlib import Path
import ocr
import image_filter_lib as flib
import os

chartfiles_path = Path(r"D:\FX\★NexT+見立てと振り返り\20250119")
if not Path(chartfiles_path).exists():
    print("指定のフォルダがありません {}".format(chartfiles_path))
    chartfiles_path = Path(os.path.expanduser('~') +r"\Desktop\make_filename_by_image_OCR\tesseract\test_samples")
    print("テストファイルで代用します {}".format(chartfiles_path))
    
for chartfile_path in [x for x in chartfiles_path.glob("*.png") if x.is_file()]:

    ocr1 = ocr.WordFromCroppedImage()
    ocr1.add_filter(flib.BlueMaskRGB())
    ocr1.ocr_language("eng")
    
    area1 = (8,10,150,44)
    text1 = ocr1.execute(chartfile_path,area1)
    
    area2 = (500,10,635,44)
    text2 = ocr1.execute(chartfile_path, area2)
    
    area3 = (1150, 10, 1270, 44)
    text3 = ocr1.execute(chartfile_path, area3)
    
    print("{}: {},{},{}".format(chartfile_path.name, text1, text2, text3))
    
