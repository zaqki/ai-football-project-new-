#!/usr/bin/env python3
"""
Football AI Video Editor - Installation Test
Tests if all dependencies are working correctly.
"""

import sys
import os
import traceback

def test_import(module_name, package_name=None, optional=False):
    """Test if a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError as e:
        status = "⚠️ " if optional else "❌"
        print(f"{status} {package_name} - {'Optional' if optional else 'Failed'}: {e}")
        return False

def test_moviepy_basic():
    """Test basic MoviePy functionality"""
    print("🎬 Testing MoviePy basic functionality...")
    try:
        from moviepy.editor import ColorClip
        # Create a simple test clip
        clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=0.1)
        print("✅ MoviePy ColorClip creation - OK")
        clip.close()
        return True
    except Exception as e:
        print(f"❌ MoviePy basic test failed: {e}")
        return False

def test_moviepy_video():
    """Test MoviePy video functionality"""
    print("🎥 Testing MoviePy video operations...")
    try:
        from moviepy.editor import ColorClip
        
        # Test video operations
        clip = ColorClip(size=(200, 200), color=(0, 255, 0), duration=0.1)
        resized_clip = clip.resize(width=100)
        cropped_clip = resized_clip.crop(x1=10, y1=10, x2=90, y2=90)
        
        print("✅ MoviePy video operations - OK")
        
        # Cleanup
        cropped_clip.close()
        resized_clip.close()
        clip.close()
        return True
    except Exception as e:
        print(f"❌ MoviePy video test failed: {e}")
        return False

def test_audio_support():
    """Test audio processing capabilities"""
    print("🎵 Testing audio support...")
    try:
        from moviepy.editor import AudioClip
        import numpy as np
        
        # Create a simple audio clip
        def make_frame(t):
            return np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        
        audio = AudioClip(make_frame, duration=0.1, fps=22050)
        print("✅ Audio processing - OK")
        audio.close()
        return True
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False

def test_ffmpeg():
    """Test FFmpeg availability"""
    print("🎬 Testing FFmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg - OK")
            return True
        else:
            print("❌ FFmpeg - Command failed")
            return False
    except Exception as e:
        print(f"❌ FFmpeg test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🏈 Football AI Video Editor - Installation Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    critical_failures = []
    
    print("📋 Testing core dependencies...")
    
    # Test critical imports
    critical_modules = [
        ("numpy", "NumPy"),
        ("PIL", "Pillow"),
        ("imageio", "ImageIO"),
        ("moviepy.editor", "MoviePy"),
    ]
    
    for module, name in critical_modules:
        if test_import(module, name):
            tests_passed += 1
        else:
            critical_failures.append(name)
        total_tests += 1
    
    # Test optional imports
    optional_modules = [
        ("av", "PyAV"),
    ]
    
    for module, name in optional_modules:
        if test_import(module, name, optional=True):
            tests_passed += 1
        total_tests += 1
    
    print("\n🧪 Testing functionality...")
    
    # Functional tests (only if critical imports passed)
    if not critical_failures:
        functional_tests = [
            (test_moviepy_basic, "MoviePy Basic"),
            (test_moviepy_video, "MoviePy Video"),
            (test_audio_support, "Audio Support"),
            (test_ffmpeg, "FFmpeg")
        ]
        
        for test_func, test_name in functional_tests:
            try:
                if test_func():
                    tests_passed += 1
                total_tests += 1
            except Exception as e:
                print(f"❌ {test_name} test crashed: {e}")
                total_tests += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if critical_failures:
        print(f"\n❌ Critical failures: {', '.join(critical_failures)}")
        print("🔧 Run: python scripts/install_requirements.py")
        return False
    elif tests_passed == total_tests:
        print("🎉 All tests passed! Your environment is ready.")
        print("\n📋 You can now run:")
        print("   python scripts/football_video_editor.py")
        return True
    else:
        print("⚠️  Some optional features may not work properly.")
        print("🔧 Consider running: python scripts/install_requirements.py")
        return True  # Still usable

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test crashed: {e}")
        traceback.print_exc()
        sys.exit(1)
