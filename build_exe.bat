:: Clear old build files
rmdir /s /q "build"
rmdir /s /q "dist"

:: Run pyinstaller
pyinstaller --noconfirm --log-level=WARN ^
    --onefile --nowindow ^
    --add-data="resources\\assets\\icons\\*:resources\\assets\icons\\" ^
    main.py
