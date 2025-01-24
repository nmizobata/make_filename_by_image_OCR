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

## ライブラリ
get_text_from_pdf(pdf_path:Path) : PDF(イメージ可)からテキストを読み取り。
get_text_from_image(image_path:Path) : イメージからテキストを読み取り
get_word_from_image(image_path:Path, area=(10,10,150,40)): エリアを指定して1語として読み取る
'''


from pathlib import Path

def poppler_path(base_dir:Path):
    return base_dir / "poppler/Library/bin"
    
def pdf2image(pdf_path:Path, output_path:Path, popplerpath:Path):
    from pdf2image import convert_from_path

    # todo: os.environコマンドは、プログラム実行がおわるとどうなるのか確認する
    # convert_from_path(pdf_path,output_folder=output_path, fmt='png',output_file=pdf_path.stem)
    pages = convert_from_path(pdf_path,poppler_path=popplerpath)
    list_pages_path = []
    for i, page in enumerate(pages):
        image_filename = pdf_path.stem + str(i)+".png"
        list_pages_path.append(output_path / image_filename)
        page.save(output_path / image_filename)
    return list_pages_path

def make_image_grayscale(list_path_images:list[Path]):
    from PIL import Image
    list_pages_path_gray = []
    for image in list_path_images:
        img = Image.open(image)
        gray_img = img.convert('L')
        working_dir = Path(__file__).parent / "image"
        gray_img_path = working_dir / (str(image.stem) + "_gray" + str(image.suffix))
        list_pages_path_gray.append(gray_img_path)
        gray_img.save(gray_img_path)
    return list_pages_path_gray

def make_image_noise_reduction(image_path:Path):
    import cv2
    import cv2_japanese   # cv2はパスに日本語が使えないので自作cv2ライブラリで処理

    # グレースケール画像を読み込む
    image = cv2_japanese.imread(image_path, 0)

    # バイラテラルフィルタでノイズ除去
    denoised_image = cv2.bilateralFilter(image, 1000, 75, 75)

    # ノイズ除去後の画像を保存
    denoised_image_path = Path(image_path).parent / ("denoised_" + Path(image_path).name)
    cv2_japanese.imwrite(denoised_image_path, denoised_image)

def get_text_from_pdf(pdf_path:Path):
    from pathlib import Path
    
    # .pdfをグレイスケールのimage(.png)に変換
    base_dir = Path(__file__).parent
    output_path = base_dir / "image"
    list_img_path = pdf2image(pdf_path, output_path, poppler_path(base_dir))
    list_gray_img_path= make_image_grayscale(list_img_path)
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

def get_word_from_image(image_path:Path, area=(10,10,150,40)):
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
    make_image_grayscale([working_dir / "cropped.png"])
    
    # ノイズ消去
    make_image_noise_reduction(working_dir / "cropped_gray.png")
    
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