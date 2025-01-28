:: Clear old build files
if exist build\ (
    rmdir /s /q "build"
)
if exist dist\ (
    rmdir /s /q "dist"
)

:: Run pyinstaller
pyinstaller --noconfirm --log-level=WARN ^
    --onefile --windowed ^
    --add-data="resources\\assets\\icons\\*:resources\\assets\icons\\" ^
    main.py
