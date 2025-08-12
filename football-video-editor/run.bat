@echo off
REM Simple setup script for Windows

echo 🏈 Football Video Editor Setup
echo ==============================

echo Step 1: Installing dependencies...
python simple_installer.py

echo.
echo Step 2: Testing installation...
python test_simple.py

echo.
echo Step 3: Creating sample files...
python create_sample_files.py

echo.
echo Step 4: Running editor...
python simple_editor.py sample_video.mp4 sample_audio.mp3

echo.
echo 🎉 Done!
pause
