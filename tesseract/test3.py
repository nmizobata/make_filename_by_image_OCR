'''
HSVによる色認識のテスト



'''
import color_detection as cd
import cv2_japanese
from pathlib import Path

basepath = Path(__file__).parent / "image"
original_imagefile = "cropped.png"
# 入力画像の読み込み
img = cv2_japanese.imread(basepath / original_imagefile)

# 色検出（赤、緑、青）
red_mask, red_masked_img = cd.detect_red_color(img)
green_mask, green_masked_img = cd.detect_green_color(img)
blue_mask, blue_masked_img = cd.detect_blue_color(img)

# 結果を出力
cv2_japanese.imwrite(basepath / "red_mask.png", red_mask)
cv2_japanese.imwrite(basepath / "red_masked_img.png", red_masked_img)
cv2_japanese.imwrite(basepath / "green_mask.png", green_mask)
cv2_japanese.imwrite(basepath / "green_masked_img.png", green_masked_img)
cv2_japanese.imwrite(basepath / "blue_mask.png", blue_mask)
cv2_japanese.imwrite(basepath / "blue_masked_img.png", blue_masked_img)