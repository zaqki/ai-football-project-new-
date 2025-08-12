#!/usr/bin/env python3
"""
Football AI Video Editor - Environment Troubleshooting Script
Verifies installation and functionality of video processing dependencies.
"""

import sys
import subprocess
import importlib
import os

def quick_install_guide():
    """Provide quick installation commands"""
    print("🚀 QUICK INSTALLATION GUIDE")
    print("=" * 40)
    print("Run these commands in your terminal:")
    print()
    print("1. pip install moviepy imageio imageio-ffmpeg av")
    print("2. python scripts/troubleshoot.py")
    print()
    print("If you're on Windows and get errors, try:")
    print("   pip install --upgrade pip")
    print("   pip install moviepy imageio imageio-ffmpeg av --no-cache-dir")
    print()
    print("If you're on macOS/Linux and get permission errors, try:")
    print("   pip install --user moviepy imageio imageio-ffmpeg av")
    print()

def check_python_version():
    """Check if Python version is 3.x"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Requires Python 3.x")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def check_ffmpeg():
    """Check if FFmpeg is available in system PATH"""
    print("🎬 Checking FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract version from first line
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg - {version_line}")
            return True
        else:
            print("❌ FFmpeg - Command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg - Not found in PATH")
        return False

def test_video_processing():
    """Test basic video processing functionality"""
    print("🧪 Testing video processing...")
    try:
        from moviepy.editor import ColorClip
        
        # Create a simple test clip
        test_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=1)
        print("✅ Video processing test - OK")
        test_clip.close()
        return True
    except Exception as e:
        print(f"❌ Video processing test - Failed: {e}")
        return False

def install_dependencies():
    """Attempt to install missing dependencies"""
    print("\n🔧 Attempting to install missing dependencies...")
    
    packages_to_install = [
        "moviepy",
        "imageio",
        "imageio-ffmpeg", 
        "av"
    ]
    
    for package in packages_to_install:
        try:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    print("🎉 All packages installed! Please run the troubleshoot script again to verify.")
    return True

def provide_installation_instructions():
    """Provide installation instructions for missing dependencies"""
    print("\n📋 INSTALLATION INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. Install Python packages:")
    print("   pip install moviepy imageio imageio-ffmpeg")
    print("   pip install av  # PyAV")
    
    print("\n2. Install FFmpeg:")
    print("   Windows: Download from https://ffmpeg.org/download.html")
    print("   macOS: brew install ffmpeg")
    print("   Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
    print("   CentOS/RHEL: sudo yum install ffmpeg")
    
    print("\n3. Verify installation:")
    print("   python troubleshoot.py")

def main():
    """Main troubleshooting function"""
    quick_install_guide()
    
    print("🏈 Football AI Video Editor - Environment Check")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 5
    
    # Check Python version
    if check_python_version():
        checks_passed += 1
    
    # Check required packages
    packages = [
        ("moviepy", "moviepy.editor"),
        ("imageio", "imageio"),
        ("PyAV", "av")
    ]
    
    missing_packages = []
    for package_name, import_name in packages:
        if check_package(package_name, import_name):
            checks_passed += 1
        else:
            missing_packages.append(package_name)
    
    # Check FFmpeg
    if check_ffmpeg():
        checks_passed += 1
    
    # Test video processing
    if checks_passed == total_checks:
        if test_video_processing():
            checks_passed += 1
            total_checks += 1
    
    print(f"\n📊 RESULTS: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 Environment is ready for Football AI Video Editor!")
        return True
    else:
        print("⚠️  Some dependencies are missing or not working properly.")
        
        # Offer to auto-install missing packages
        if missing_packages:
            print(f"\nMissing packages: {', '.join(missing_packages)}")
            response = input("\n🤖 Would you like me to try installing missing packages automatically? (y/n): ")
            
            if response.lower() in ['y', 'yes']:
                if install_dependencies():
                    print("\n🔄 Please run this script again to verify the installation.")
                    return True
        
        provide_installation_instructions()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
