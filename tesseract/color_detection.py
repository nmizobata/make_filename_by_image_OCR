'''
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
import cv2
import cv2_japanese
import numpy as np
from typing import Literal
from pathlib import Path
COLOR_DETECTION = Literal["NA","inverted","red_mask","red_mased_image","green_mask","green_masked_image","blue_mask","blue_masked_image","blue_minus_black_mask","blue_minus_black_masked_image"]


def make_image_color_detection(mode:COLOR_DETECTION, img_path:Path):
    working_dir = Path(__file__).parent / "image"
    img = cv2_japanese.imread(img_path)
    if mode=="NA":
        return img_path
    if mode=="red_mask":
        red_mask, red_masked_img = detect_red_color(img)
        cv2_japanese.imwrite(working_dir / "red_mask.png", red_mask)
        return working_dir / "red_mask.png"
    if mode=="red_masked_image":
        red_mask, red_masked_img = detect_red_color(img)
        cv2_japanese.imwrite(working_dir / "red_masked_img.png", red_masked_img)
        return working_dir / "red_masked_img.png"
    if mode=="green_mask":
        green_mask, green_masked_img = detect_green_color(img)
        cv2_japanese.imwrite(working_dir / "green_mask.png", green_mask)
        return working_dir / "green_mask.png"
    if mode=="green_masked_image":
        green_mask, green_masked_img = detect_green_color(img)
        cv2_japanese.imwrite(working_dir / "green_masked_img.png", green_masked_img)
        return working_dir / "green_masked_img.png"
    if mode=="blue_mask":
        blue_mask, blue_masked_img = detect_blue_color(img)
        cv2_japanese.imwrite(working_dir / "blue_mask.png", blue_mask)
        return working_dir / "blue_mask.png"
    if mode=="blue_masked_image":
        blue_mask, blue_masked_img = detect_blue_color(img)
        cv2_japanese.imwrite(working_dir / "blue_masked_img.png", blue_masked_img)
        return working_dir / "blue_masked_img.png"
    if mode=="blue_minus_black_mask":
        blue_minus_black_mask, blue_minus_black_masked_img = detect_blue_minus_black_color(img)
        cv2_japanese.imwrite(working_dir / "blue_minus_black_mask.png", blue_minus_black_mask)
        return working_dir / "blue_minus_black_mask.png"
    if mode=="blue_minus_black_masked_image":
        blue_minus_black_mask, blue_minus_black_masked_img = detect_blue_minus_black_color(img)
        cv2_japanese.imwrite(working_dir / "blue_minus_black_masked_img.png", blue_minus_black_masked_img)
        return working_dir / "blue_minus_black_masked_img.png"
    if mode=="inverted":
        inverted_img = image_inverted(img)
        cv2_japanese.imwrite(working_dir / "inverted_img.png", inverted_img)
        return working_dir / "inverted_img.png"
 

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