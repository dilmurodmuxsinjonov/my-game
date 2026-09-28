@echo off
title Voxel Lord: Feudal Realm - Master Launcher
color 0A
cls

echo ===============================================================================
echo            VOXEL LORD: FEUDAL REALM - MASTER GAME LAUNCHER
echo      First-Person Medieval Voxel Colony Simulator (Godot 4.3 / C++ Core)
echo ===============================================================================
echo.

:: 1. Search for Godot Executable
set GODOT_EXE=
where godot.exe >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set GODOT_EXE=godot.exe
    goto FOUND_GODOT
)

if exist "godot.exe" (
    set GODOT_EXE=godot.exe
    goto FOUND_GODOT
)

if exist "C:\Godot\godot.exe" (
    set GODOT_EXE=C:\Godot\godot.exe
    goto FOUND_GODOT
)

if exist "C:\Program Files\Godot\godot.exe" (
    set GODOT_EXE="C:\Program Files\Godot\godot.exe"
    goto FOUND_GODOT
)

for /f "delims=" %%I in ('dir /b /s "%USERPROFILE%\Downloads\Godot_v4*.exe" 2^>nul') do (
    set GODOT_EXE="%%I"
    goto FOUND_GODOT
)

:: If not found in standard paths:
echo [!] Godot 4.3 binary was not found in standard system paths.
echo.
echo Please choose an option below:
echo   [1] Launch Instant Interactive Playable Simulator (Python Engine)
echo   [2] Run Full 300+ Automated Test Suite
echo   [3] Install Godot Engine automatically via Windows Package Manager (winget)
echo   [4] Launch custom Godot executable (Enter custom path)
echo   [5] Exit
echo.
set /p USER_CHOICE="Enter selection [1-5]: "

if "%USER_CHOICE%"=="1" goto LAUNCH_SIMULATOR
if "%USER_CHOICE%"=="2" goto RUN_TESTS
if "%USER_CHOICE%"=="3" goto INSTALL_GODOT
if "%USER_CHOICE%"=="4" goto PROMPT_CUSTOM
if "%USER_CHOICE%"=="5" exit /b 0
goto LAUNCH_SIMULATOR

:FOUND_GODOT
echo [*] Located Godot engine at: %GODOT_EXE%
echo [*] Launching Voxel Lord: Feudal Realm (res://scenes/main.tscn)...
echo.
%GODOT_EXE% --path "%~dp0." res://scenes/main.tscn
pause
exit /b 0

:LAUNCH_SIMULATOR
echo.
echo [*] Launching Standalone Interactive Playable Simulator...
python "%~dp0tools\interactive_play_simulator.py"
pause
exit /b 0

:RUN_TESTS
echo.
echo [*] Running full test suite...
python -m unittest discover -s "%~dp0tests" -p "test_*.py"
pause
exit /b 0

:INSTALL_GODOT
echo.
echo [*] Attempting to install GodotEngine via winget...
winget install GodotEngine.GodotEngine
echo.
echo [*] Installation finished. Re-running launcher...
pause
goto :FOUND_GODOT

:PROMPT_CUSTOM
echo.
set /p CUSTOM_PATH="Enter full path to godot.exe: "
if exist "%CUSTOM_PATH%" (
    set GODOT_EXE="%CUSTOM_PATH%"
    goto FOUND_GODOT
) else (
    echo [ERROR] File does not exist at: %CUSTOM_PATH%
    pause
    exit /b 1
)
