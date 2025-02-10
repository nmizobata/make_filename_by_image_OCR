'''
研究用イメージの取得(NexT+見立てと振り返りチャート)からイメージを取得し、croped.png名でimageフォルダに保存。
cropping機能を必要に応じて使用。

取得したイメージは適当に名前を変えて、image_stockに保存しておくと研究用に使用できる。
'''

from pathlib import Path

def get_cropped_imagefile(image_path:Path,area: tuple)->Path:
    from pathlib import Path
    from PIL import Image

    # image cropping
    working_dir = Path(__file__).parent / "image"
    img=Image.open(image_path)
    
    image_path = working_dir / "cropped.png"
    img.crop(area).save(image_path)
    return image_path
    
if __name__ == '__main__':
    imagefiles_path = Path(r"D:\FX\★NexT+見立てと振り返り\20250119")
    imagefile = "87CHFJPY.png"
    image_path = imagefiles_path / imagefile
    if not Path(image_path).exists():
        print("ファイルが存在しません {}".format(image_path))
    else:
        # エリア指定
        area = (8,10,150,44)      # 6枚チャート
        # area = (500,10,635,42)  # 7枚クロスチャート
        # area = (1150, 10, 1270, 42)   # 7枚クロスチャート
        # area = (13,480,100,510)  # EURGBP, Monthly
        image_path = get_cropped_imagefile(image_path, area)
    
