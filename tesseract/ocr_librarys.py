'''
ocrライブラリで使用するツールライブラリ集

必要なバイナリライブラリ
- poppler(pdf->image変換): https://github.com/oschwartz10612/poppler-windows/releases/ からダウンロード/解凍の上、popplerフォルダに格納する。
- tesseract(OCR): https://github.com/UB-Mannheim/tesseract/wiki からインストーラを入手し、インストールする (Additional script data, Additional langudate dataでJapaneseを選択する)

installが必要なpythonライブラリ
- conda install pdf2image(pillowも必要だがまとめてインストールされる)
- conda install pyocr

利用している自作ライブラリ
- cv2_japanese.py

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

def make_images_grayscale(list_path_images:list[Path])->list[Path]:
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

def make_image_grayscale(image_path:Path)->Path:
    from PIL import Image
    
    image = Image.open(image_path)
    gray_image = image.convert('L')
    working_dir = Path(__file__).parent / "image"
    gray_image_path = working_dir / ("gray_" + Path(image_path).name)
    # list_pages_path_gray.append(gray_image_path)
    gray_image.save(gray_image_path)
    return gray_image_path

def make_image_noise_reduction(image_path:Path)->Path:
    import cv2
    import cv2_japanese   # cv2はパスに日本語が使えないので自作cv2ライブラリで処理

    # グレースケール画像を読み込む
    image = cv2_japanese.imread(image_path, 0)

    # バイラテラルフィルタでノイズ除去
    denoised_image = cv2.bilateralFilter(image, 15, 75, 75)

    # ノイズ除去後の画像を保存
    denoised_image_path = Path(image_path).parent / ("denoised_" + Path(image_path).name)
    cv2_japanese.imwrite(denoised_image_path, denoised_image)
    return denoised_image_path

def make_image_high_resolution(image_path:Path)->Path:
    import cv2
    import cv2_japanese

    # 画像を読み込む
    image = cv2_japanese.imread(image_path)

    # 現在の解像度を確認
    height, width = image.shape[:2]
    print(f'元の解像度: {width} x {height}')

    # 解像度を300dpiに調整
    new_height = int(height * (600 / 96))  # 96dpiから300dpiへ
    new_width = int(width * (600 / 96))
    resized_image = cv2.resize(image, (new_width, new_height))

    # 調整後の解像度を確認
    print(f'調整後の解像度: {new_width} x {new_height}')

    # 調整後の画像を保存
    hireso_image_path = Path(image_path).parent / ("hireso_" + Path(image_path).name)
    cv2_japanese.imwrite(hireso_image_path, resized_image)
    return hireso_image_path

def make_image_binary(image_path:Path)->Path:
    import cv2
    import cv2_japanese

    # ノイズ除去後の画像を読み込む
    image = cv2_japanese.imread(image_path, 0)

    # 大津の方法で二値化
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 二値化した画像を保存
    binary_image_path = Path(image_path).parent / ("binary_" + Path(image_path).name)
    cv2_japanese.imwrite(binary_image_path, binary_image)
    return binary_image_path