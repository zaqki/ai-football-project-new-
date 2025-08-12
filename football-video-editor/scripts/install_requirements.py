#!/usr/bin/env python3
"""
Football AI Video Editor - Requirements Installer
Automatically installs all required dependencies.
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("⚠️  This project requires Python 3.7 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("📦 Upgrading pip...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True, text=True)
        print("✅ pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  pip upgrade failed, continuing anyway: {e.stderr}")
        return False

def install_package(package, retry_count=2):
    """Install a single package with retry logic"""
    package_name = package.split(">=")[0]
    
    for attempt in range(retry_count + 1):
        try:
            print(f"📦 Installing {package_name}... (attempt {attempt + 1})")
            
            # Different installation strategies
            if attempt == 0:
                # Standard installation
                cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
            elif attempt == 1:
                # Try with --no-cache-dir
                cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade", "--no-cache-dir"]
            else:
                # Try with --user flag
                cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade", "--user"]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ {package_name} installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            if attempt < retry_count:
                print(f"⚠️  Attempt {attempt + 1} failed, trying different approach...")
            else:
                print(f"❌ Failed to install {package_name} after {retry_count + 1} attempts")
                print(f"Error: {e.stderr}")
                return False
    
    return False

def check_system_dependencies():
    """Check for system-level dependencies"""
    print("🔍 Checking system dependencies...")
    
    # Check for FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg not found - some features may not work")
        print("   Install FFmpeg from: https://ffmpeg.org/download.html")

def main():
    """Install all required packages"""
    print("🏈 Football AI Video Editor - Installing Dependencies")
    print("=" * 55)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check system dependencies
    check_system_dependencies()
    
    # Upgrade pip
    upgrade_pip()
    
    # Required packages in order of dependency
    packages = [
        "numpy>=1.21.0",
        "pillow>=8.0.0",
        "imageio>=2.25.0",
        "imageio-ffmpeg>=0.4.8",
        "moviepy>=1.0.3",
        "av>=10.0.0"
    ]
    
    print(f"\n📋 Installing {len(packages)} required packages...")
    
    success_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages, 1):
        package_name = package.split(">=")[0]
        print(f"\n[{i}/{len(packages)}] Installing {package_name}...")
        
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package_name)
    
    print(f"\n📊 Installation Results:")
    print(f"✅ Successful: {success_count}/{len(packages)} packages")
    
    if failed_packages:
        print(f"❌ Failed: {', '.join(failed_packages)}")
    
    if success_count == len(packages):
        print("\n🎉 All dependencies installed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python scripts/test_installation.py")
        print("2. Then: python scripts/football_video_editor.py")
        return True
    else:
        print(f"\n⚠️  {len(failed_packages)} packages failed to install.")
        print("\n🔧 Manual installation options:")
        print("1. Try: pip install moviepy imageio imageio-ffmpeg av")
        print("2. Or: conda install -c conda-forge moviepy imageio av")
        print("3. Check your internet connection and try again")
        
        if failed_packages:
            print(f"\nSpecifically failed: {', '.join(failed_packages)}")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
