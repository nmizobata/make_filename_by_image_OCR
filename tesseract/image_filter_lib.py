'''
イメージフィルタ集。
cv2, Pillowを使用。

# 使用方法
import image_filter
import image_filter_lib

ifilter = image_filter.ImageFilter()
ifilter.add(NoiseReduction())
ifilter.add(reversed())
ifilter.execute(image_path_org, display)

## 参考
HSVによる画像の色認識とマスキング処理
https://python.joho.info/opencv/opencv-color-detection/

## 準備
installが必要なpythonライブラリ
- pip install opencv-python
- pip install opencv-contrib-python(拡張機能。今回は利用していない)

利用している自作ライブラリ
- cv2_japanese

## ライブラリ
def make_image_color_detection(mode: COLOR_DETECTION, image_path: Path)

参考
https://qiita.com/hsgucci/items/e9a65d4fa3d279e4219e


'''

#-*- coding:utf-8 -*-
from abc import ABC, abstractmethod

import cv2
import cv2_japanese
import numpy as np
# from typing import Literal
from pathlib import Path
# COLOR_DETECTION = Literal["NA","inverted","red_mask","red_mased_image","green_mask","green_masked_image","blue_mask","blue_masked_image","blue_minus_black_mask","blue_minus_black_masked_image"]



class ImageFilterLib(ABC):
    def __init__(self, image_path:Path=""):
        self.image_path = image_path
        self.serial_number = ""
        self.working_dir = Path(__file__).parent / "image"
    
    def set_image_path(self,image_path:Path):
        self.image_path = image_path
        
    def set_serial_number(self, number):
        self.serial_number = str(number)+"_"
    
    @abstractmethod
    def __str__(self):
        pass
        
    @abstractmethod
    def execute():
        pass

class Inverted(ImageFilterLib):
    def __str__(self):
        return "Inverted"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            img_inverted = image_inverted(img)
            new_image_path = self.working_dir / (self.serial_number+"inverted.png")
            cv2_japanese.imwrite(new_image_path, img_inverted)
            return new_image_path

class Grayscale(ImageFilterLib):
    def __str__(self):
        return "Grayscale"
    
    def execute(self):
        from PIL import Image
        
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            image = Image.open(self.image_path)
            gray_image = image.convert('L')
            gray_image_path = self.working_dir / (self.serial_number+"grayscale.png")
            gray_image.save(gray_image_path)
            return gray_image_path
    
class NoiseReduction(ImageFilterLib):
    def __str__(self):
        return "NoiseReduction"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            # グレースケール画像を読み込む
            image = cv2_japanese.imread(self.image_path, 0)

            # バイラテラルフィルタでノイズ除去
            denoised_image = cv2.bilateralFilter(image, 15, 75, 75)

            # ノイズ除去後の画像を保存
            denoised_image_path = self.working_dir / (self.serial_number+"denoised.png")
            cv2_japanese.imwrite(denoised_image_path, denoised_image)
            return denoised_image_path
        
class HighResolution(ImageFilterLib):
    def __str__(self):
        return "HighResolution"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            # 画像を読み込む
            image = cv2_japanese.imread(self.image_path)

            # 現在の解像度を確認
            height, width = image.shape[:2]
            print(f'元の解像度: {width} x {height}')

            # 解像度を600dpiに調整
            new_height = int(height * (600 / 96))  # 96dpiから600dpiへ
            new_width = int(width * (600 / 96))
            resized_image = cv2.resize(image, (new_width, new_height))

            # 調整後の解像度を確認
            print(f'調整後の解像度: {new_width} x {new_height}')

            # 調整後の画像を保存
            hireso_image_path = self.working_dir / (self.serial_number+"hiresolution.png")
            cv2_japanese.imwrite(hireso_image_path, resized_image)
            return hireso_image_path
        
class Binarization(ImageFilterLib):
    def __str__(self):
        return "Binarization"

    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            image = cv2_japanese.imread(self.image_path, 0)

            # 大津の方法で二値化
            _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 二値化した画像を保存
            binary_image_path = self.working_dir / (self.serial_number+"binarization.png")
            cv2_japanese.imwrite(binary_image_path, binary_image)
            return binary_image_path

class RedMaskHSV(ImageFilterLib):    
    def __str__(self):
        return "Red Mask(HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            red_mask, _ = detect_red_color(img)
            new_image_path = self.working_dir / (self.serial_number+"red_mask.png")
            cv2_japanese.imwrite(new_image_path, red_mask)
            return new_image_path
        

class RedMaskedHSV(ImageFilterLib):
    def __str__(self):
        return "Red Masked Image (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            _, red_masked = detect_red_color(img)
            new_image_path = self.working_dir / (self.serial_number+"red_masked_image.png")
            cv2_japanese.imwrite(new_image_path, red_masked)
            return new_image_path

class GreenMaskHSV(ImageFilterLib):
    def __str__(self):
        return "Green Mask (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            green_mask, _ = detect_green_color(img)
            new_image_path = self.working_dir / (self.serial_number+"green_mask.png")
            cv2_japanese.imwrite(new_image_path, green_mask)
            return new_image_path

class GreenMaskedHSV(ImageFilterLib):
    def __str__(self):
        return "Green Masked Image (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            _, green_masked = detect_green_color(img)
            new_image_path = self.working_dir / (self.serial_number+"green_masked_image.png")
            cv2_japanese.imwrite(new_image_path, green_masked)
            return new_image_path

class BlueMaskHSV(ImageFilterLib):
    def __str__(self):
        return "Blue Mask (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            blue_mask, _ = detect_blue_color(img)
            new_image_path = self.working_dir / (self.serial_number+"blue_mask.png")
            cv2_japanese.imwrite(new_image_path, blue_mask)
            return new_image_path

class BlueMaskedHSV(ImageFilterLib):
    def __str__(self):
        return "Blue Masked Image (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            _, blue_masked = detect_blue_color(img)
            new_image_path = self.working_dir / (self.serial_number+"blue_masked_image.png")
            cv2_japanese.imwrite(new_image_path, blue_masked)
            return new_image_path
class BlueMinusBlackMaskHSV(ImageFilterLib):
    def __str__(self):
        return "Blue minus Black Mask (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            blue_minus_black_mask, _ = detect_blue_minus_black_color(img)
            new_image_path = self.working_dir / (self.serial_number+"blue_minus_black_mask.png")
            cv2_japanese.imwrite(new_image_path, blue_minus_black_mask)
            return new_image_path
class BlueMinusBlackMasedHSV(ImageFilterLib):
    def __str__(self):
        return "Blue minus Black Masked Image (HSV)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            _, blue_minus_black_masked = detect_blue_minus_black_color(img)
            new_image_path = self.working_dir / (self.serial_number+"blue_minus_black_masked_image.png")
            cv2_japanese.imwrite(new_image_path, blue_minus_black_masked)
            return new_image_path
class RedMaskRGB(ImageFilterLib):
    pass
class RedMaskedRGB(ImageFilterLib):
    pass
class GreenMaskRGB(ImageFilterLib):
    pass
class GreenMaskedRGB(ImageFilterLib):
    pass
class BlueMaskRGB(ImageFilterLib):
    def __str__(self):
        return "Blue Mask (RGB)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            blue_mask_RGB, _ = detect_blue_color_on_RGB(img)
            new_image_path = self.working_dir / (self.serial_number+"blue_mask_RGB.png")
            cv2_japanese.imwrite(new_image_path, blue_mask_RGB)
            return new_image_path
class BlueMaskedRGB(ImageFilterLib):
    def __str__(self):
        return "Blue Masked Image (RGB)"
    
    def execute(self):
        if not Path(self.image_path).exists():
            print("ファイルが見つかりません:{}".format(self.image_path))
        else:
            img = cv2_japanese.imread(self.image_path)
            _, blue_masked_RGB = detect_blue_color_on_RGB(img)
            new_image_path = self.working_dir / (self.serial_number+"blue_masked_image_RGB.png")
            cv2_japanese.imwrite(new_image_path, blue_masked_RGB)
            return new_image_path

# 赤色の検出
def detect_red_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,64,0])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,64,0])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色領域のマスク（255：赤色、0：赤色以外）
    mask = mask1 + mask2

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

# 緑色の検出
def detect_green_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域1
    hsv_min = np.array([30, 64, 0])
    hsv_max = np.array([90,255,255])

    # 緑色領域のマスク（255：赤色、0：赤色以外）
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

# 青色の検出
def detect_blue_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 青色のHSVの値域1
    # hsv_min = np.array([90, 64, 0])
    hsv_min = np.array([90, 64, 0])
    hsv_max = np.array([150,255,255])

    # 青色領域のマスク（255：赤色、0：赤色以外）
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

# 青色反転マスクによるマスキング処理
def detect_blue_color_inverted(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 青色のHSVの値域1
    # hsv_min = np.array([90, 64, 0])
    hsv_min = np.array([90, 64, 0])
    hsv_max = np.array([150,255,255])

    # 青色領域のマスク（255：赤色、0：赤色以外）
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask_inverted = cv2.bitwise_not(mask)

    # マスキング処理
    masked_img = cv2.bitwise_or(img, img, mask=mask_inverted)

    return mask_inverted, masked_img

def detect_blue_minus_black_color(img):
    # 青色mask
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 青色のHSVの値域1
    hsv_min = np.array([90, 64, 0])
    hsv_max = np.array([150,255,255])
    mask_blue = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,64,0])
    hsv_max = np.array([30,255,255])
    mask_red1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,64,0])
    hsv_max = np.array([179,255,255])
    mask_red2 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 緑色のHSVの値域1
    hsv_min = np.array([30, 64, 0])
    hsv_max = np.array([90,255,255])
    mask_green = cv2.inRange(hsv, hsv_min, hsv_max)

    mask = mask_blue - mask_red1 - mask_red2 - mask_green
    
    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

def detect_blue_color_on_RGB(img):
    import cv2
    import numpy as np

    # BGR形式で青色の範囲を指定
    lower_blue = np.array([100, 0, 0])
    upper_blue = np.array([255, 50, 50])

    # マスクを作成
    mask = cv2.inRange(img, lower_blue, upper_blue)

    # 元の画像とマスクを使って青色部分を抽出
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img
    # 結果を表示

# ネガポジ反転
def image_inverted(img):
    image_inverted = cv2.bitwise_not(img)
    return image_inverted

if __name__ == '__main__':
    working_dir = Path(__file__).parent / "image"
    imagefile = "0_cropped.png"
    if not Path(working_dir / imagefile).exists():
        print("imageフォルダに[0_cropping.png]を保存してください")
    
    # 入力画像の読み込み
    imagefile_path = working_dir / imagefile
    img = cv2_japanese.imread(imagefile_path)

    # 色検出（赤、緑、青）
    red_mask, red_masked_img = detect_red_color(img)
    green_mask, green_masked_img = detect_green_color(img)
    blue_mask, blue_masked_img = detect_blue_color(img)
    blue_minus_black_mask, blue_minus_black_masked_img = detect_blue_minus_black_color(img)
    blue_mask_inverted, blue_mask_inverted_img = detect_blue_color_inverted(img)
    blue_mask_on_RGB, blue_masked_img_on_RGB = detect_blue_color_on_RGB(img)

    # 結果を出力
    cv2_japanese.imwrite(working_dir / "red_mask.png", red_mask)
    cv2_japanese.imwrite(working_dir / "red_masked_img.png", red_masked_img)
    cv2_japanese.imwrite(working_dir / "green_mask.png", green_mask)
    cv2_japanese.imwrite(working_dir / "green_masked_img.png", green_masked_img)
    cv2_japanese.imwrite(working_dir / "blue_mask.png", blue_mask)
    cv2_japanese.imwrite(working_dir / "blue_masked_img.png", blue_masked_img)
    cv2_japanese.imwrite(working_dir / "blue_minus_black_mask.png", blue_minus_black_mask)
    cv2_japanese.imwrite(working_dir / "blue_minus_black_masked_img.png", blue_minus_black_masked_img)
    cv2_japanese.imwrite(working_dir / "blue_mask_inverted.png", blue_mask_inverted)
    cv2_japanese.imwrite(working_dir / "blue_mask_inverted_img.png", blue_mask_inverted_img)
    cv2_japanese.imwrite(working_dir / "blue_mask_on_RGB.png", blue_mask_on_RGB)
    cv2_japanese.imwrite(working_dir / "blue_masked_img_on_RGB.png", blue_masked_img_on_RGB)