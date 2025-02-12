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
    # def __init__(self, pdf_path:Path):
    #     super().__init__()
    #     self.pdf_path = pdf_path

    def execute(self, pdf_path: Path)->list:
        poppler_path = Path(__file__).parent / "poppler/Library/bin"
        working_dir = Path(__file__).parent / "image"
        list_img_path = glib.pdf2image(pdf_path, working_dir, poppler_path)
        
        list_text = []
        for image_path in list_img_path:
            TextDetect = TextFromImage()
            text = TextDetect.execute(image_path)
            list_text.append(text)
        return list_text
        
class TextFromImage(Ocr):
    # def __init__(self, image_path:Path):
    #     super().__init__()
    #     self.image_path = image_path
    
    def execute(self, image_path: Path)->str:
        
        # 画像のフィルタリング処理
        image_path=self.execute_filter(image_path)
        #  OCR処理
        text = execute_tesseract(image_path, self.ocr_lang, 6)
        
        # # tesseract.exeのパスを通します。
        # # 文字認識したい画像を開きます。
        # img=Image.open(self.image_path)

        # # Tesseractで文字認識します。
        return text
    
class WordFromCroppedImage(Ocr):
    # def __init__(self, image_path:Path, area=(10,10,150,40)):
    #     super().__init__()
    #     self.image_path = image_path
    #     self.area = area
    
    def execute(self, image_path:Path, area=(0,0,0,0))->str:
        from PIL import Image

        working_dir = Path(__file__).parent / "image"
        # 画像を指定のエリアで切り取りして保存。
        img=Image.open(image_path)
        if area == (0,0,0,0):
            img_width, img_height = img.size
            area = (0,0,img_width, img_height)
        img.crop(area).save(working_dir / "cropped.png")
        image_path = working_dir / "cropped.png"
        
        # 切り取り画像のフィルタリング処理
        image_path=self.execute_filter(image_path)

        #  OCR処理
        text = execute_tesseract(image_path, self.ocr_lang, 8)

        return text

def execute_tesseract(image_path:Path, language:str, tesseract_layout_mode:int)->str:
    import os
    import pyocr
    from PIL import Image
    
    # tesseract.exeのパスを通します。
    pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # Tesseractで文字認識します。
    img=Image.open(image_path)
    builder = pyocr.builders.TextBuilder(tesseract_layout_mode)
    text = tool.image_to_string(img,lang=language,builder=builder)

    return text
'''
0	文字角度の識別と書字系のみの認識(OSD)のみ実施（outputbase.osdが出力され、OCRは行われない）
1	OSDと自動ページセグメンテーション
2	OSDなしの自動セグメンテーション（OCRは行われない）
3	OSDなしの完全自動セグメンテーション（デフォルト）
4	可変サイズの1列テキストを想定する
5	縦書きの単一のテキストブロックとみなす
6	単一のテキストブロックとみなす（5と異なる点は横書きのみ）
7	画像を1行のテキストとみなす
8	画像を単語とみなす
9	円の中に記載された1単語とみなす（例：①、⑥など）
10	画像を1文字とみなす
11	まだらなテキスト。特定の順序でなるべく多くの単語を検出する（角度無し）
12	文字角度検出を実施(OSD)しかつ、まだらなテキストとしてなるべく多くの単語を検出する
13	Tesseract固有の処理を回避して1行のテキストとみなす
'''

if __name__=="__main__":
    from pathlib import Path
    import image_filter_lib as iflib
    
    working_path = Path(__file__).parent / "image"
    pdf_path = Path(__file__).parent / "test_samples" / "sample.pdf"
    pdfocr = TextFromPdf()
    pdfocr.add_filter(iflib.NoiseReduction())
    text = pdfocr.execute(pdf_path)
    print(text)
    
    img_path = Path(__file__).parent / "test_samples" / "03AUDクロス-EQRAUD.png"
    wordocr = WordFromCroppedImage()
    wordocr.add_filter(iflib.BlueMaskedRGB())
    word = wordocr.execute(img_path)
    print(word)
    
    img_path = Path(__file__).parent / "test_samples" / "87CHFJPY.png"
    area = (8,10,150,44)
    word = wordocr.execute(img_path, area)
    print(word)