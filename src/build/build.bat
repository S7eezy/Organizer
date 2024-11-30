@echo off
REM Save the current directory path
set CURRENT_DIR=%cd%

REM Navigate to the src directory where main.pyw is located
cd ..

REM Remove previous dist folder and main.spec file if they exist
if exist dist rd /s /q dist
if exist main.spec del /f /q main.spec

REM Build the executable using PyInstaller
pyinstaller --onefile --windowed ^
--icon=gui\assets\logos\icon.ico ^
--name=Organizer ^
--add-data "gui;gui" ^
--add-data "core;core" ^
main.pyw

REM Move the built executable to the desired location
if exist ..\Organizer.exe del /f /q ..\Organizer.exe
move dist\Organizer.exe ..\Organizer.exe

REM Clean up build files
if exist dist rd /s /q dist
if exist main.spec del /f /q main.spec

REM Navigate back to the build directory
cd "%CURRENT_DIR%"

echo Build completed successfully. The executable is located at ..\Organizer.exe
pause
