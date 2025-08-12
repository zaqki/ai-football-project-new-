#!/usr/bin/env python3
"""
Simple Football Video Editor
"""

import os
import sys

# Check dependencies first
def check_moviepy():
    try:
        import moviepy.editor
        return True
    except ImportError:
        print("❌ MoviePy not found!")
        print("Run: python simple_installer.py")
        return False

if not check_moviepy():
    sys.exit(1)

# Now import moviepy
from moviepy.editor import VideoFileClip, AudioFileClip

class SimpleVideoEditor:
    def __init__(self):
        self.width = 608
        self.height = 1080
    
    def process_video(self, video_file, audio_file, output_file="output.mp4"):
        """Process video with audio"""
        print("🏈 Starting video processing...")
        
        # Check files exist
        if not os.path.exists(video_file):
            print(f"❌ Video file not found: {video_file}")
            return False
            
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return False
        
        try:
            print("📹 Loading video...")
            video = VideoFileClip(video_file)
            
            print("🎵 Loading audio...")
            audio = AudioFileClip(audio_file)
            
            print("🔄 Syncing audio to video length...")
            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)
            elif audio.duration < video.duration:
                # Loop audio to match video
                loops = int(video.duration / audio.duration) + 1
                audio = audio.loop(n=loops).subclip(0, video.duration)
            
            print("📱 Resizing for vertical format...")
            # Simple resize to vertical
            video_resized = video.resize(height=self.height)
            
            # Center crop to target width
            w, h = video_resized.size
            if w > self.width:
                x_center = w // 2
                x_start = x_center - (self.width // 2)
                video_resized = video_resized.crop(x1=x_start, x2=x_start + self.width)
            
            print("🎭 Adding audio to video...")
            final_video = video_resized.set_audio(audio)
            
            print("💾 Exporting video...")
            final_video.write_videofile(
                output_file,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"🎉 Success! Output saved as: {output_file}")
            
            # Cleanup
            video.close()
            audio.close()
            final_video.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def main():
    editor = SimpleVideoEditor()
    
    # Look for default files
    video_files = ["heskey skill and finish.mp4", "isak_goal.mp4"]
    audio_file = "isak_voice.mp3"
    
    # Find video file
    video_path = None
    for vf in video_files:
        if os.path.exists(vf):
            video_path = vf
            break
    
    if not video_path:
        print("❌ No video file found!")
        print("Please add one of these files:")
        for vf in video_files:
            print(f"  - {vf}")
        print("\nOr run with custom files:")
        print("  python simple_editor.py <video> <audio>")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    # Process video
    success = editor.process_video(video_path, audio_file)
    return success

if __name__ == "__main__":
    # Allow custom files as arguments
    if len(sys.argv) == 3:
        video_file = sys.argv[1]
        audio_file = sys.argv[2]
        editor = SimpleVideoEditor()
        success = editor.process_video(video_file, audio_file)
        sys.exit(0 if success else 1)
    else:
        success = main()
        sys.exit(0 if success else 1)
