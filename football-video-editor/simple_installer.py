#!/usr/bin/env python3
"""
Simple installer for Football Video Editor
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a single package"""
    print(f"Installing {package}...")
    try:
        # Try standard install first
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package} (standard attempt). Error: {e}")
        print(f"Trying with --no-cache-dir...")
        try:
            # Try with --no-cache-dir
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--no-cache-dir"])
            print(f"✅ {package} installed successfully (with --no-cache-dir)")
            return True
        except subprocess.CalledProcessError as e_nocache:
            print(f"❌ Failed to install {package} (no-cache attempt). Error: {e_nocache}")
            print(f"Trying with --user...")
            try:
                # Try with --user
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
                print(f"✅ {package} installed successfully (with --user)")
                return True
            except subprocess.CalledProcessError as e_user:
                print(f"❌ Failed to install {package} (user attempt). Error: {e_user}")
                return False

def main():
    print("🏈 Installing Football Video Editor Dependencies")
    print("=" * 50)
    
    # Upgrade pip first for best compatibility
    print("📦 Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip upgraded successfully")
    except Exception as e:
        print(f"⚠️  Failed to upgrade pip, continuing anyway: {e}")

    # Essential packages
    packages = [
        "moviepy",
        "imageio", 
        "imageio-ffmpeg",
        "numpy", # Often a dependency for moviepy/imageio
        "Pillow" # Often a dependency for imageio
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    if success_count == len(packages):
        print(f"\n🎉 All {success_count} core packages installed!")
        print("Now, let's re-run the test report to confirm:")
        print("  python generate_test_report.py")
    else:
        print(f"\n⚠️ Only {success_count}/{len(packages)} core packages installed successfully.")
        print("Please review the errors above. You might need to try manual installation:")
        print("  pip install moviepy imageio imageio-ffmpeg numpy Pillow")
        print("Then re-run the test report: python generate_test_report.py")

if __name__ == "__main__":
    main()
