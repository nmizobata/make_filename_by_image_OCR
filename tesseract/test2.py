
from pathlib import Path
import ocr
# import cv2_japanese
# import cv2

chartfiles_path = Path(__file__).parent / "image"
chartfile = "cropped.png"

chartfile_path = chartfiles_path / chartfile
# print(chartfile_path)
ocr.make_images_grayscale([chartfile_path])

# グレースケール画像を読み込む
# chartfile = "cropped_gray.png"
# chartfile_path = chartfiles_path / chartfile
# print(chartfile_path)
# image = cv2_japanese.imread(chartfile_path)

# バイラテラルフィルタでノイズ除去
# denoised_image = cv2.bilateralFilter(image, 15, 75, 75)

# chartfile = "denoised_cropped_gray.png"
# chartfile_path = chartfiles_path / chartfile
# ノイズ除去後の画像を保存
# cv2_japanese.imwrite(chartfile_path, denoised_image)
ocr.make_image_noise_reduction(chartfile_path)