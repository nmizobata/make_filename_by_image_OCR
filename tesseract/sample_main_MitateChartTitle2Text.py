'''
日々の見立てチャートファイルのファイル名自動変換
EUR等のクロスチャートやGBPAUD等のマルチタイムチャートの画像ファイルのファイル名を自動付加する


'''
from pathlib import Path
import ocr
import image_filter_lib as flib

chartfiles_path = Path(r"D:\FX\★NexT+見立てと振り返り\20250119")
if not Path(chartfiles_path).exists():
    print("指定のフォルダがありません {}".format(chartfiles_path))
    
for chartfile_path in [x for x in chartfiles_path.glob("*.png") if x.is_file()]:
    area1 = (8,10,150,44)
    ocr1 = ocr.WordFromCroppedImage(chartfile_path,area1)
    ocr1.add_filter(flib.BlueMaskRGB())
    ocr1.ocr_language("eng")
    text1 = ocr1.execute()
    
    area2 = (500,10,635,44)
    ocr2 = ocr.WordFromCroppedImage(chartfile_path,area2)
    ocr2.add_filter(flib.BlueMaskRGB())
    ocr2.ocr_language("eng")
    text2 = ocr2.execute()
    
    area3 = (1150, 10, 1270, 44)
    ocr3 = ocr.WordFromCroppedImage(chartfile_path,area3)
    ocr3.add_filter(flib.BlueMaskRGB())
    ocr3.ocr_language("eng")
    text3 = ocr3.execute()
    
    print("{}: {},{},{}".format(chartfile_path.name, text1, text2, text3))
    
