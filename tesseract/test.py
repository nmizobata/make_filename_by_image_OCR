from pathlib import Path
import ocr

chartfiles_path = Path("D:\FX\★NexT+見立てと振り返り")
chartfile = "07CHFクロス.png"

chartfile_path = chartfiles_path / chartfile
print(chartfile_path)
# area = (10,10,150,40)
# area = (500,10,635,40)
area = (1150, 10, 1270, 35)
text = ocr.get_word_from_image(chartfile_path,area)    
print("{}: {}".format(chartfile_path.name, text))
