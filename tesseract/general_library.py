'''
応用範囲がひろい一般的な自作ライブラリ集

'''
from pathlib import Path

def delete_all_file_in_working_dir(working_dir:Path, exclude: list=[]):
    '''
    指定フォルダ内のファイルをすべて消す。(除外指定可能)
    
    * imput
    working_dir (Path): 対象のフォルダ
    exclude (list[str]): 削除しないファイルのファイル名をリストで与える
    '''
    for file in [x for x in working_dir.iterdir() if x.is_file()]:
        if file.name not in exclude:
            print("delete {} ...".format(file.name))
            file.unlink()
            
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