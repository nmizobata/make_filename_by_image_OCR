# Image OCRでファイル名を変更
## 概要
imageを文字認識して、ファイル名を生成する。
応用編として、pdfファイルをimageに変換したうえで文字認識することも考える。

## インストールが必要なバイナリライブラリ
1. poppler(pdf->image変換): 
https://github.com/oschwartz10612/poppler-windows/releases/ からダウンロード/解凍の上、popplerフォルダに格納する。
2. tesseract(OCR): 
https://github.com/UB-Mannheim/tesseract/wiki からインストーラを入手し、インストールする (Additional script data, Additional langudate dataでJapaneseを選択する)

## インストールが必要なpythonライブラリ
1. pdf2image (pdf -> image変換)
- conda install pdf2image(pillowも必要だがまとめてインストールされる)
2. pyocr (イメージの文字認識)
- conda install pyocr
3. opencv-python
- pip install opencv-python (2025/2/1時点 condaではインストールできない模様)

利用している自作ライブラリ
- cv2_japanese.py