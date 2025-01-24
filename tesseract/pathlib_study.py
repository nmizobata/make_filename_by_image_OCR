# __file__を基準にPathを操作することで、ディレクトリ環境が変わっても同じコードが利用できる。

from pathlib import Path

p=Path(".")  # 現ディレクトリのPathオブジェクトを得る
# Pathオブジェクトを現実の世界に持ち込むためにはメソッドで変換が必要

# absolute(): 現ディレクトリの絶対パスの文字列を得る
print("現ディレクトリ{}".format(p.absolute()))

# resolve(): 現ディレクトリの絶対パスの文字列を得る
print("現ディレクトリ{}".format(p.resolve()))

# .cwd():  Pathオブジェクトの内容に関係なく、現在のディレクトリを得る
print("現ディレクトリ{}".format(Path("/a/a/a/").cwd()))

# iterdir(): 現ディレクトリ内のファイルやディレクトリを得る(iterdir()はイテレータオブジェクトなので、リスト化する必要がある)
files_and_dirs_itr = p.iterdir()
for file_and_dir in files_and_dirs_itr:
    print("現ディレクトリの中身:{}".format(file_and_dir))
    
# rglob(): ワイルドカード検索→イテレータオブジェクト 現ディレクトリだけでなくサブディレクトリのものも検出する。
# glob():  ワイルドカード検索→イテレータオプジェクト 現ディレクトリだけで検出する。
files_py = p.rglob("*.py")
for file_py in files_py:
    print("現ディレクトリの.pyファイル:{}".format(file_py))

# 補.サブディレクトのみを取り出したい場合はリスト内表記で条件付けする
for dirname in [x for x in p.iterdir() if x.is_dir()]:
    print("現ディレクトリのサブディレクトリ:{}".format(dirname))

# 補.ファイルのみを取り出したい場合はリスト内表記で条件付けする
for filename in [x for x in p.iterdir() if x.is_file()]:
    print("現ディレクトリのファイル:{}".format(filename))
# その他、symboolicfile等の条件式あり。

# 補.指定の*.png

# パス文字列のみを操作したい場合はPathオブジェクトで用意されているプロパティを利用する。ただし文字列操作のみなので注意。
path_text = "c:hoge/hoge2/hoge3.txt"
print("-----パス文字列操作-----")
print("元のパス文字列(path):              {}".format(path_text))
print("path.parent:                       {}".format(Path(path_text).parent))
print("path.parent.parent:                {}".format(Path(path_text).parent.parent))
print("path.parent.parent.parent:         {}".format(Path(path_text).parent.parent.parent))
print("path.parent.parent.parent.parent:  {}".format(Path(path_text).parent.parent.parent.parent))
print("拡張子の置き換えtxt->hoge:         {}".format(Path(path_text).with_suffix(".hoge")))
print("ファイル名の置き換えhoge3→hoge999: {}".format(Path(path_text).with_name("hoge999.txt")))
print("子ディレクトリの追加:              {}".format(Path(path_text) / "hogehoge.txt"))  #! "/hogehoge.txt"としてはいけないことに注意
print("ドライブ名:                        {}, type:{}".format(Path(path_text).drive,type(Path(path_text).drive)))
print("ファイル名:                        {}, type:{}".format(Path(path_text).name,type(Path(path_text).name)))
print("拡張子除くファイル名               {}, type:{}".format(Path(path_text).stem,type(Path(path_text).name)))
print("拡張子:                           {}".format(Path(path_text).suffix))
new_filename = Path(path_text).parent / (Path(path_text).stem+"_new"+Path(path_text).suffix)  #! ファイル名を弄る場合(文字列計算をする場合)はカッコでくくること
print("新しいファイル名でパス作成:         {}".format(new_filename))
print("パスの各パーツを分離したもの        {}".format(Path(path_text).parts))
