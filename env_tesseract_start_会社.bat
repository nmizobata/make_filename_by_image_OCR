ECHO 
ECHO minicondaの設定および仮想環境の自動起動
ECHO 仮想環境を終了する場合は"deactivate"を実行

set minicondapath=C:\Users\fx22228.DC00\AppData\Local\miniconda3
set kankyo=tesseract
set drive=c:

%drive%
%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %minicondapath% & activate %kankyo%"
