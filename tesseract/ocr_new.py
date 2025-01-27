'''
PDFファイルおよびイメージファイル内のテキストをOCRでよみとり返すライブラリ。
PDFは一度イメージに変換してからOCRを行う。
## 準備
必要なバイナリライブラリ
- poppler(pdf->image変換): https://github.com/oschwartz10612/poppler-windows/releases/ からダウンロード/解凍の上、popplerフォルダに格納する。
- tesseract(OCR): https://github.com/UB-Mannheim/tesseract/wiki からインストーラを入手し、インストールする (Additional script data, Additional langudate dataでJapaneseを選択する)

installが必要なpythonライブラリ
- conda install pdf2image(pillowも必要だがまとめてインストールされる)
- conda install pyocr

利用している自作ライブラリ
- ocr_library.py
- color_detection.py

## ライブラリ
class TextFromPdf(pdf_path:Path) : PDF(イメージ可)からテキストを読み取るクラス
class TextFromImage(image_path:Path) :  イメージからテキストを読み取り
class WordFromCroppedIma(image_path:Path, area=(10,10,150,40)): 切り取りエリアを指定して1語として読み取る
上記はいずれもテキスト認識前に前処理(グレイスケール化、ノイズリダクション、カラー認識)を選択可能。

def get_text_from_pdf(pdf_path:Path) : PDF(イメージ可)からテキストを読み取り。
def get_text_from_image(image_path:Path) : イメージからテキストを読み取り
def get_word_from_cropped_image(image_path:Path, area=(10,10,150,40)): 切り取りエリアを指定して1語として読み取る
'''


from abc import ABC, abstractmethod
from pathlib import Path
import ocr_librarys as lib
import color_detection as cd
from typing import Literal

COLOR_DETECTION = Literal["NA","inverted","red_mask","red_mased_image","green_mask","green_masked_image","blue_mask","blue_masked_image","blue_minus_black_mask","blue_minus_black_masked_image"]
LANGUAGE = Literal["eng+jpn","eng","jpn"]

class Ocr(ABC):
    def __init__(self):
        self.apply_grayscale = False
        self.apply_noise_reduction = False
        self.apply_color_detection = "NA"
        self.ocr_lang = "jpn"
        
    def grayscale(self, apply: bool = False):
        self.apply_grayscale = apply

    def noise_reduction(self, apply: bool = False):
        self.apply_noise_reduction = apply
        
    def color_detection(self, apply: COLOR_DETECTION= "NA"):
        self.apply_color_detection = apply
    
    def image_filter(self, image_path):
        if self.apply_grayscale:
            image_path = lib.make_image_grayscale(image_path)
        if self.apply_noise_reduction:
            image_path = lib.make_image_noise_reduction(image_path)
        if self.apply_color_detection!="NA":
            image_path = cd.make_image_color_detection(self.apply_color_detection,image_path)
        return image_path
    
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
        list_img_path = lib.pdf2image(self.pdf_path, working_dir, poppler_path)
        
        list_text = []
        for image_path in list_img_path:
            TextDetect = TextFromImage(image_path)
            TextDetect.grayscale(self.apply_grayscale)
            TextDetect.noise_reduction(self.apply_noise_reduction)
            TextDetect.color_detection(self.apply_color_detection)
            text = TextDetect.execute()
            # text = get_text_from_image(image_path)
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
        
        self.image_path=self.image_filter(self.image_path)
        
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
        self.image_path=self.image_filter(self.image_path)

        # tesseract.exeのパスを通します。
        pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"
        tools = pyocr.get_available_tools()
        tool = tools[0]

        # Tesseractで文字認識します。
        img=Image.open(self.image_path)
        builder = pyocr.builders.TextBuilder(tesseract_layout=8)
        text = tool.image_to_string(img,lang=self.ocr_lang,builder=builder)

        return text


def get_text_from_pdf(pdf_path:Path):
    from pathlib import Path
    
    # .pdfをグレイスケールのimage(.png)に変換
    base_dir = Path(__file__).parent
    output_path = base_dir / "image"
    list_img_path = lib.pdf2image(pdf_path, output_path, lib.poppler_path(base_dir))
    list_gray_img_path= lib.make_images_grayscale(list_img_path)
    # print(list_gray_img_path)
    
    # imageファイルに対しOCR
    list_text = []
    for image in list_gray_img_path:
        text = get_text_from_image(image)
        list_text.append(text)
    return list_text

def get_text_from_image(image_path:Path):
    import pyocr
    from PIL import Image
    import os
    
    # tesseract.exeのパスを通します。
    pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"

    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 文字認識したい画像を開きます。
    img=Image.open(image_path)

    # Tesseractで文字認識します。
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    text = tool.image_to_string(img,lang="jpn",builder=builder)

    return text

def get_word_from_cropped_image(image_path:Path, area=(10,10,150,40)):
    import pyocr
    from PIL import Image
    import os.path
    from pathlib import Path

    working_dir = Path(__file__).parent / "image"

    # tesseract.exeのパスを通します。
    pyocr.tesseract.TESSERACT_CMD = os.path.expanduser('~') + r"\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # os.path.expanduser('~')="C:\Users\blues\"
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 画像を指定のエリアで切り取りして保存。
    img=Image.open(image_path)
    img.crop(area).save(working_dir / "cropped.png")

    # グレイスケール変換
    lib.make_image_grayscale(working_dir / "cropped.png")
    
    # ノイズ消去
    lib.make_image_noise_reduction(working_dir / "cropped_gray.png")
    
    # Tesseractで文字認識します。
    denoised_img_gray=Image.open(working_dir / "denoised_cropped_gray.png")
    builder = pyocr.builders.TextBuilder(tesseract_layout=8)
    text = tool.image_to_string(denoised_img_gray,lang="jpn",builder=builder)

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
        