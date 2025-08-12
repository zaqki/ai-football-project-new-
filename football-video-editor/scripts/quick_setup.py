#!/usr/bin/env python3
"""
Football AI Video Editor - Quick Setup Script
One-click setup for the entire video editor environment.
"""

import sys
import subprocess
import os

def run_script(script_name, description):
    """Run a Python script and return success status"""
    print(f"\n🚀 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    """Main setup function"""
    print("🏈 Football AI Video Editor - Quick Setup")
    print("=" * 50)
    print("This script will:")
    print("1. Install all required dependencies")
    print("2. Verify the installation")
    print("3. Test the video editor")
    print()
    
    input("Press Enter to continue...")
    
    # Step 1: Install dependencies
    if not run_script("scripts/install_dependencies.py", "Installing Dependencies"):
        print("❌ Dependency installation failed. Please check the errors above.")
        return False
    
    # Step 2: Verify installation
    if not run_script("scripts/troubleshoot.py", "Verifying Installation"):
        print("❌ Installation verification failed. Please check the errors above.")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 You can now use:")
    print("• python scripts/football_video_editor.py - Main video editor")
    print("• python scripts/video_analyzer.py <video> - Analyze videos")
    print("• python scripts/batch_processor.py <dir> <audio> - Batch process")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
