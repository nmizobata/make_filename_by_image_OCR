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