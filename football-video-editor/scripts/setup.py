#!/usr/bin/env python3
"""
Football AI Video Editor - Complete Setup Script
One command to set up everything.
"""

import sys
import subprocess
import os

def print_header(title):
    """Print a formatted header"""
    print(f"\n🏈 {title}")
    print("=" * (len(title) + 3))

def run_script(script_path, description):
    """Run a Python script"""
    print(f"\n🚀 {description}...")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Complete setup process"""
    print_header("Football AI Video Editor - Complete Setup")
    
    print("This will:")
    print("1. 📦 Install all required dependencies")
    print("2. 🧪 Test the installation")
    print("3. 📋 Show you how to use the editor")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Install requirements
    print_header("Step 1: Installing Dependencies")
    if not run_script("scripts/install_requirements.py", "Installing packages"):
        print("❌ Installation failed. Please check the errors above.")
        return False
    
    # Step 2: Test installation
    print_header("Step 2: Testing Installation")
    if not run_script("scripts/test_installation.py", "Testing installation"):
        print("❌ Tests failed. Please check the errors above.")
        return False
    
    # Step 3: Success message
    print_header("Setup Complete!")
    print("🎉 Your Football AI Video Editor is ready to use!")
    
    print("\n📋 How to use:")
    print("1. Place your video files (heskey skill and finish.mp4 or isak_goal.mp4)")
    print("2. Place your audio file (isak_voice.mp3)")
    print("3. Run: python scripts/football_video_editor.py")
    
    print("\n🔧 Other tools:")
    print("• Analyze videos: python scripts/video_analyzer.py <video_file>")
    print("• Custom processing: python scripts/football_video_editor.py <video> <audio>")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
