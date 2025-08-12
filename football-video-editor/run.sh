#!/bin/bash
# Simple setup script for Linux/Mac

echo "🏈 Football Video Editor Setup"
echo "=============================="

echo "Step 1: Installing dependencies..."
python3 simple_installer.py

echo -e "\nStep 2: Testing installation..."
python3 test_simple.py

echo -e "\nStep 3: Creating sample files..."
python3 create_sample_files.py

echo -e "\nStep 4: Running editor..."
python3 simple_editor.py sample_video.mp4 sample_audio.mp3

echo -e "\n🎉 Done!"
