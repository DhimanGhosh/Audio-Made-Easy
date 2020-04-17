if %1% == "kv" (
    cd GUI
)

if %1% == "qt" (
    cd GUI_QT
)
python MusicTheoryGuide.py
cd ..\
