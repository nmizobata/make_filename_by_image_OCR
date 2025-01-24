'''
日々の見立てチャートファイルのファイル名自動変換
EUR等のクロスチャートやGBPAUD等のマルチタイムチャートの画像ファイルのファイル名を自動付加する


'''
from pathlib import Path
import ocr

chartfiles_path = Path("D:\FX\★NexT+見立てと振り返り")
for chartfile_path in [x for x in chartfiles_path.glob("*.png") if x.is_file()]:
    # print(chartfile_path)
    area1 = (10,10,150,40)
    text1 = ocr.get_word_from_image(chartfile_path,area1)
    
    area2 = (500,10,635,40)
    text2 = ocr.get_word_from_image(chartfile_path,area2)
    
    area3 = (1150, 10, 1270, 40)
    text3 = ocr.get_word_from_image(chartfile_path,area3)
    
    print("{}: {},{},{}".format(chartfile_path.name, text1, text2, text3))
    
