#!/usr/bin/env python3
"""
Football AI Video Editor - Dependency Installation Script
Automatically installs all required dependencies for the video editor.
"""

import sys
import subprocess
import os

def install_package(package_name, display_name=None):
    """Install a single package using pip"""
    if display_name is None:
        display_name = package_name
    
    print(f"📦 Installing {display_name}...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", package_name, "--upgrade"
        ], check=True, capture_output=True, text=True)
        
        print(f"✅ {display_name} installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {display_name}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main installation function"""
    print("🏈 Football AI Video Editor - Dependency Installer")
    print("=" * 55)
    
    # List of required packages
    packages = [
        ("moviepy", "MoviePy (Video editing library)"),
        ("imageio", "ImageIO (Image/Video I/O)"),
        ("imageio-ffmpeg", "ImageIO FFmpeg plugin"),
        ("av", "PyAV (Video processing)")
    ]
    
    print("📋 Installing required packages...")
    print("This may take a few minutes...\n")
    
    successful_installs = 0
    total_packages = len(packages)
    
    for package_name, display_name in packages:
        if install_package(package_name, display_name):
            successful_installs += 1
        print()  # Empty line for readability
    
    print("=" * 55)
    print(f"📊 Installation Results: {successful_installs}/{total_packages} packages installed")
    
    if successful_installs == total_packages:
        print("🎉 All dependencies installed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python scripts/troubleshoot.py")
        print("2. Then: python scripts/football_video_editor.py")
        return True
    else:
        print("⚠️  Some packages failed to install.")
        print("\n🔧 Manual installation:")
        print("Try running: pip install moviepy imageio imageio-ffmpeg av")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
