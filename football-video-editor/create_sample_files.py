#!/usr/bin/env python3
"""
Create sample video and audio files for testing
"""

import os

def create_sample_video():
    """Create a sample video file"""
    print("🎬 Creating sample video...")
    
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        
        # Create a simple colored background
        background = ColorClip(size=(1280, 720), color=(0, 100, 0), duration=5)
        
        # Add text
        try:
            text = TextClip("Sample Football Video", fontsize=50, color='white', font='Arial')
            text = text.set_position('center').set_duration(5)
            video = CompositeVideoClip([background, text])
        except:
            # If text fails, just use background
            video = background
        
        # Save sample video
        video.write_videofile("sample_video.mp4", fps=24, verbose=False, logger=None)
        video.close()
        
        print("✅ Sample video created: sample_video.mp4")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample video: {e}")
        return False

def create_sample_audio():
    """Create a sample audio file"""
    print("🎵 Creating sample audio...")
    
    try:
        import numpy as np
        from moviepy.editor import AudioClip
        
        # Create a simple tone
        def make_frame(t):
            return np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        
        audio = AudioClip(make_frame, duration=5, fps=22050)
        audio.write_audiofile("sample_audio.mp3", verbose=False, logger=None)
        audio.close()
        
        print("✅ Sample audio created: sample_audio.mp3")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample audio: {e}")
        return False

def main():
    print("🏈 Creating Sample Files for Testing")
    print("=" * 40)
    
    # Check if MoviePy is available
    try:
        import moviepy.editor
    except ImportError:
        print("❌ MoviePy not found!")
        print("Run: python simple_installer.py")
        return False
    
    video_success = create_sample_video()
    audio_success = create_sample_audio()
    
    if video_success and audio_success:
        print("\n🎉 Sample files created!")
        print("Now run: python simple_editor.py sample_video.mp4 sample_audio.mp3")
        return True
    else:
        print("\n⚠️ Some sample files failed to create")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
