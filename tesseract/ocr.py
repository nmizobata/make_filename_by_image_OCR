'''
PDFファイルおよびイメージファイル内のテキストをOCRでテキスト認識。
PDFは一度イメージに変換してからOCRを行う。


利用している自作ライブラリ
- image_filter.py
- general_library

## ライブラリ
class TextFromPdf(pdf_path:Path) : PDF(イメージ可)からテキストを読み取るクラス
class TextFromImage(image_path:Path) :  イメージからテキストを読み取り
class WordFromCroppedImage(image_path:Path, area=(10,10,150,40)): 切り取りエリアを指定して1語として読み取る
上記はいずれもテキスト認識前に前処理(グレイスケール化、ノイズリダクション、カラー認識)を選択可能。

'''


from abc import ABC, abstractmethod
from pathlib import Path
import general_library as glib
import image_filter as imf
from typing import Literal


# COLOR_DETECTION = Literal["NA","inverted","red_mask","red_masked_image","green_mask","green_masked_image","blue_mask","blue_masked_image","blue_minus_black_mask","blue_minus_black_masked_image"]
LANGUAGE = Literal["eng+jpn","eng","jpn"]

class Ocr(ABC):
    def __init__(self):
        self.imagefilter = imf.ImageFilter()
        self.ocr_lang = "jpn"
    
    
    def add_filter(self, filter):
        self.imagefilter.add(filter)
    
    def execute_filter(self, image_path):
        return self.imagefilter.execute(image_path)
    
    def ocr_language(self, lang:LANGUAGE="jpn"):
        self.ocr_lang = lang
        
    @abstractmethod
    def execute(self):
        pass
    
class TextFromPdf(Ocr):
    def __init__(self, pdf_path:Path):
        super().__init__()
        self.pdf_path = pdf_path

    def execute(self)->list:
        poppler_path = Path(__file__).parent / "poppler/Library/bin"
        working_dir = Path(__file__).parent / "image"
        list_img_path = glib.pdf2image(self.pdf_path, working_dir, poppler_path)
        
        list_text = []
        for image_path in list_img_path:
            TextDetect = TextFromImage(image_path)
            text = TextDetect.execute()
            list_text.append(text)
        return list_text
        
class TextFromImage(Ocr):
    def __init__(self, image_path:Path):
        super().__init__()
        self.image_path = image_path
    
    def execute(self)->str:
        import pyocr
        from PIL import Image
        import os
        
        self.image_path=self.execute_filter(self.image_path)
        
        # tesseract.exeのパスを通します。
        pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"

        tools = pyocr.get_available_tools()
        tool = tools[0]

        # 文字認識したい画像を開きます。
        img=Image.open(self.image_path)

        # Tesseractで文字認識します。
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        text = tool.image_to_string(img,lang=self.ocr_lang,builder=builder)

        return text
    
class WordFromCroppedImage(Ocr):
    def __init__(self, image_path:Path, area=(10,10,150,40)):
        super().__init__()
        self.image_path = image_path
        self.area = area
        
    def execute(self)->str:
        import pyocr
        from PIL import Image
        import os.path

        working_dir = Path(__file__).parent / "image"
        # 画像を指定のエリアで切り取りして保存。
        img=Image.open(self.image_path)
        img.crop(self.area).save(working_dir / "cropped.png")
        self.image_path = working_dir / "cropped.png"
        
        # 切り取り画像のフィルタリング処理
        self.image_path=self.execute_filter(self.image_path)

        # tesseract.exeのパスを通します。
        pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"
        tools = pyocr.get_available_tools()
        tool = tools[0]

        # Tesseractで文字認識します。
        img=Image.open(self.image_path)
        builder = pyocr.builders.TextBuilder(tesseract_layout=8)
        text = tool.image_to_string(img,lang=self.ocr_lang,builder=builder)

        return text


'''
Memo: pyocr.builders.TextBuilder(tesseract_layout=NN) NNにOCRモード番号を指定。各モードの内容以下の通り
Page segmentation modes:
   0    Orientation and script detection (OSD) only.
   1    Automatic page segmentation with OSD.
   2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
   3    Fully automatic page segmentation, but no OSD. (Default)
   4    Assume a single column of text of variable sizes.
   5    Assume a single uniform block of vertically aligned text.
   6    Assume a single uniform block of text.
   7    Treat the image as a single text line.
   8    Treat the image as a single word.
   9    Treat the image as a single word in a circle.
  10    Treat the image as a single character.
  11    Sparse text. Find as much text as possible in no particular order.
  12    Sparse text with OSD.
  13    Raw line. Treat the image as a single text line,
        bypassing hacks that are Tesseract-specific.


'''
        