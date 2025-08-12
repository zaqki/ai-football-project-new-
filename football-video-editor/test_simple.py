#!/usr/bin/env python3
"""
Test if everything is working
"""

def test_imports():
    """Test if we can import required modules"""
    print("🧪 Testing imports...")
    
    try:
        import moviepy.editor
        print("✅ MoviePy - OK")
    except ImportError as e:
        print(f"❌ MoviePy - Failed: {e}")
        return False
    
    try:
        import imageio
        print("✅ ImageIO - OK")
    except ImportError as e:
        print(f"❌ ImageIO - Failed: {e}")
        return False
    
    return True

def test_moviepy():
    """Test basic MoviePy functionality"""
    print("🎬 Testing MoviePy...")
    
    try:
        from moviepy.editor import ColorClip
        clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=0.1)
        print("✅ MoviePy test - OK")
        clip.close()
        return True
    except Exception as e:
        print(f"❌ MoviePy test failed: {e}")
        return False

def main():
    print("🏈 Testing Football Video Editor")
    print("=" * 40)
    
    if not test_imports():
        print("\n❌ Import tests failed")
        print("Run: python simple_installer.py")
        return False
    
    if not test_moviepy():
        print("\n❌ MoviePy test failed")
        return False
    
    print("\n🎉 All tests passed!")
    print("You can now run: python simple_editor.py")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
