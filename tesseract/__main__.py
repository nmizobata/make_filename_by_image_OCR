'''
PDFファイル内のテキストを一旦イメージに変換して、OCRで取り出す。
PDFファイルは、tesseract/pdf/に格納する。
ocrは自作ライブラリ。
20250124 K1.0 
'''

from pathlib import Path
import ocr_new

pdf_name = "sample.pdf"

base_dir = Path(__file__).parent
pdf_path = base_dir / "pdf" / pdf_name
    
# text_list = ocr_new.get_text_from_pdf(pdf_path)
ocr = ocr_new.TextFromPdf(pdf_path)
ocr.grayscale(True)
text_list = ocr.execute()

for text in text_list:
    print(text)
    
