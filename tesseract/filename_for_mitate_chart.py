'''
日々の見立てチャートファイルのファイル名自動変換
EUR等のクロスチャートやGBPAUD等のマルチタイムチャートの画像ファイルのファイル名を自動付加する


'''
from pathlib import Path
import ocr_new

chartfiles_path = Path(r"D:\FX\★NexT+見立てと振り返り\20250119")
if not Path(chartfiles_path).exists():
    print("指定のフォルダがありません {}".format(chartfiles_path))
    
for chartfile_path in [x for x in chartfiles_path.glob("*.png") if x.is_file()]:
    # print(chartfile_path)
    area1 = (8,10,150,44)
    ocr1 = ocr_new.WordFromCroppedImage(chartfile_path,area1)
    ocr1.color_detection("blue_mask")
    text1 = ocr1.execute()
    # text1 = ocr_new.get_word_from_cropped_image(chartfile_path,area1)
    
    area2 = (500,10,635,44)
    ocr2 = ocr_new.WordFromCroppedImage(chartfile_path,area2)
    ocr2.color_detection("blue_mask")
    text2 = ocr2.execute()
    # text2 = ocr_new.get_word_from_cropped_image(chartfile_path,area2)
    
    area3 = (1150, 10, 1270, 44)
    ocr3 = ocr_new.WordFromCroppedImage(chartfile_path,area3)
    ocr3.color_detection("blue_mask")
    text3 = ocr3.execute()
    # text3 = ocr_new.get_word_from_cropped_image(chartfile_path,area3)
    
    print("{}: {},{},{}".format(chartfile_path.name, text1, text2, text3))
    
