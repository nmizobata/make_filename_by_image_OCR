rem Pythonファイルの起動用バッチファイル
rem kankyo変数に仮想環境名を入力
rem pypath *.pyファイルがあるディレクトリパス

set minicondapath=C:\Users\fx22228.DC00\AppData\Local\miniconda3
set kankyo=XXXXXXX
set python=YYYYYYY.py
set pypath=C:\Users\fx22228.DC00\Documents\PythonScripts\XXXXXXX

cd %pypath%
%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %kankyo%&python %python%"

rem pause
