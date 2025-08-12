#!/usr/bin/env python3
"""
Football AI Video Editor - Quick Start
One command to install, test, and run the editor.
"""

import sys
import subprocess
import os
from pathlib import Path

def run_script(script_name, description):
    """Run a script and return success status"""
    print(f"\n🚀 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, f"scripts/{script_name}"], 
                              capture_output=False)
        success = result.returncode == 0
        if success:
            print(f"✅ {description} completed successfully")
        else:
            print(f"❌ {description} failed")
        return success
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def check_sample_files():
    """Check if sample files exist"""
    video_files = ["heskey skill and finish.mp4", "isak_goal.mp4"]
    audio_file = "isak_voice.mp3"
    
    found_video = None
    for video in video_files:
        if os.path.exists(video):
            found_video = video
            break
    
    audio_exists = os.path.exists(audio_file)
    
    print(f"\n📁 Sample files check:")
    if found_video:
        print(f"✅ Video file found: {found_video}")
    else:
        print(f"❌ No video files found. Looking for: {', '.join(video_files)}")
    
    if audio_exists:
        print(f"✅ Audio file found: {audio_file}")
    else:
        print(f"❌ Audio file not found: {audio_file}")
    
    return found_video is not None and audio_exists

def main():
    """Quick start process"""
    print("🏈 Football AI Video Editor - Quick Start")
    print("=" * 50)
    
    print("This will:")
    print("1. 📦 Install all dependencies")
    print("2. 🧪 Test the installation")
    print("3. 🎬 Run the video editor (if files are available)")
    
    response = input("\nContinue? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '']:
        print("❌ Cancelled by user")
        return False
    
    # Step 1: Install dependencies
    if not run_script("install_requirements.py", "Installing Dependencies"):
        print("\n❌ Installation failed. Please check the errors above.")
        return False
    
    # Step 2: Test installation
    if not run_script("test_installation.py", "Testing Installation"):
        print("\n❌ Tests failed. Please check the errors above.")
        return False
    
    # Step 3: Check for sample files and run editor
    print("\n🎬 Checking for sample files...")
    if check_sample_files():
        print("\n🚀 Running Football Video Editor...")
        return run_script("football_video_editor.py", "Processing Video")
    else:
        print("\n📋 Setup complete! To use the editor:")
        print("1. Add your video file (heskey skill and finish.mp4 or isak_goal.mp4)")
        print("2. Add your audio file (isak_voice.mp3)")
        print("3. Run: python scripts/football_video_editor.py")
        print("\nOr use custom files:")
        print("   python scripts/football_video_editor.py <video_file> <audio_file>")
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
