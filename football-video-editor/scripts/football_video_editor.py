#!/usr/bin/env python3
"""
Football AI Video Editor - Main Processing Script
Merges football highlight videos with voiceovers and formats for social media.
"""

import os
import sys
from pathlib import Path

# Dependency check with helpful error message
def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import moviepy.editor
    except ImportError:
        missing_deps.append("moviepy")
    
    try:
        import imageio
    except ImportError:
        missing_deps.append("imageio")
    
    if missing_deps:
        print("❌ Missing required dependencies!")
        print(f"Missing: {', '.join(missing_deps)}")
        print("\n🔧 To fix this:")
        print("1. Run: python scripts/install_requirements.py")
        print("2. Or manually: pip install moviepy imageio imageio-ffmpeg av")
        print("3. Then run this script again")
        return False
    
    return True

# Only import after dependency check
if not check_dependencies():
    sys.exit(1)

from moviepy.editor import VideoFileClip, AudioFileClip

class FootballVideoEditor:
    def __init__(self):
        self.target_width = 608
        self.target_height = 1080
        self.output_codec = 'libx264'
        self.audio_codec = 'aac'
    
    def validate_files(self, video_path, audio_path):
        """Validate that input files exist and are accessible"""
        print("📁 Validating input files...")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"✅ Video file: {video_path}")
        print(f"✅ Audio file: {audio_path}")
    
    def load_media(self, video_path, audio_path):
        """Load video and audio files"""
        print("🎬 Loading media files...")
        
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            print(f"📹 Video duration: {video.duration:.2f}s, Size: {video.size}")
            print(f"🎵 Audio duration: {audio.duration:.2f}s")
            
            return video, audio
        
        except Exception as e:
            raise RuntimeError(f"Failed to load media files: {e}")
    
    def synchronize_audio(self, video, audio):
        """Synchronize audio duration to match video"""
        print("🔄 Synchronizing audio with video...")
        
        video_duration = video.duration
        audio_duration = audio.duration
        
        if abs(video_duration - audio_duration) < 0.1:
            print("✅ Audio and video durations already match")
            return audio
        
        if audio_duration > video_duration:
            # Trim audio to match video
            print(f"✂️  Trimming audio from {audio_duration:.2f}s to {video_duration:.2f}s")
            audio = audio.subclip(0, video_duration)
        else:
            # Loop audio to match video duration
            print(f"🔁 Looping audio from {audio_duration:.2f}s to {video_duration:.2f}s")
            loops_needed = int(video_duration / audio_duration) + 1
            audio = audio.loop(n=loops_needed).subclip(0, video_duration)
        
        return audio
    
    def format_for_vertical(self, video):
        """Resize video to vertical format (608x1080)"""
        print(f"📱 Formatting video for vertical display ({self.target_width}x{self.target_height})...")
        
        original_width, original_height = video.size
        original_ratio = original_width / original_height
        target_ratio = self.target_width / self.target_height
        
        print(f"Original size: {original_width}x{original_height} (ratio: {original_ratio:.2f})")
        print(f"Target size: {self.target_width}x{self.target_height} (ratio: {target_ratio:.2f})")
        
        if original_ratio > target_ratio:
            # Video is wider than target - fit by height and crop sides
            new_height = self.target_height
            new_width = int(original_width * (self.target_height / original_height))
            
            # Resize and center crop
            resized_video = video.resize(height=new_height)
            x_center = new_width // 2
            x_start = x_center - (self.target_width // 2)
            
            formatted_video = resized_video.crop(x1=x_start, x2=x_start + self.target_width)
            
        else:
            # Video is taller than target - fit by width and crop top/bottom
            new_width = self.target_width
            new_height = int(original_height * (self.target_width / original_width))
            
            # Resize and center crop
            resized_video = video.resize(width=new_width)
            y_center = new_height // 2
            y_start = y_center - (self.target_height // 2)
            
            formatted_video = resized_video.crop(y1=y_start, y2=y_start + self.target_height)
        
        print(f"✅ Video formatted to {formatted_video.size}")
        return formatted_video
    
    def merge_video_audio(self, video, audio):
        """Merge video with synchronized audio"""
        print("🎭 Merging video with audio...")
        
        # Set the audio of the video
        final_video = video.set_audio(audio)
        
        print("✅ Video and audio merged successfully")
        return final_video
    
    def export_video(self, video, output_path):
        """Export the final video with specified codecs"""
        print(f"💾 Exporting video to {output_path}...")
        
        try:
            video.write_videofile(
                output_path,
                codec=self.output_codec,
                audio_codec=self.audio_codec,
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            print(f"🎉 Video exported successfully: {output_path}")
            
            # Get file size
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"📊 File size: {file_size:.2f} MB")
            
        except Exception as e:
            raise RuntimeError(f"Failed to export video: {e}")
    
    def process_video(self, video_path, audio_path, output_path="final_output.mp4"):
        """Main processing pipeline"""
        print("🏈 Starting Football AI Video Editor")
        print("=" * 50)
        
        video = None
        audio = None
        
        try:
            # Step 1: Validate files
            self.validate_files(video_path, audio_path)
            
            # Step 2: Load media
            video, audio = self.load_media(video_path, audio_path)
            
            # Step 3: Synchronize audio
            synchronized_audio = self.synchronize_audio(video, audio)
            
            # Step 4: Format for vertical
            vertical_video = self.format_for_vertical(video)
            
            # Step 5: Merge video and audio
            final_video = self.merge_video_audio(vertical_video, synchronized_audio)
            
            # Step 6: Export
            self.export_video(final_video, output_path)
            
            print("\n🎊 Processing completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during processing: {e}")
            return False
        
        finally:
            # Clean up resources
            if video:
                video.close()
            if audio:
                audio.close()
        
        return True

def main():
    """Main function with example usage"""
    editor = FootballVideoEditor()
    
    # Example with provided files
    video_files = ["heskey skill and finish.mp4", "isak_goal.mp4"]
    audio_file = "isak_voice.mp3"
    
    # Try to find available video file
    video_path = None
    for video_file in video_files:
        if os.path.exists(video_file):
            video_path = video_file
            break
    
    if not video_path:
        print("❌ No video files found. Please ensure one of these files exists:")
        for video_file in video_files:
            print(f"   - {video_file}")
        print("\n💡 You can also specify custom files:")
        print("   python scripts/football_video_editor.py <video_file> <audio_file>")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        print("Please ensure the audio file exists in the current directory.")
        return False
    
    # Process the video
    success = editor.process_video(video_path, audio_file)
    
    if success:
        print("\n📱 Your vertical football highlight video is ready for social media!")
        print("   - Format: 608x1080 (vertical)")
        print("   - Codecs: H.264 video, AAC audio")
        print("   - Compatible with: TikTok, Instagram Reels, YouTube Shorts")
    
    return success

if __name__ == "__main__":
    # Allow custom video and audio files as command line arguments
    if len(sys.argv) == 3:
        video_file = sys.argv[1]
        audio_file = sys.argv[2]
        
        if os.path.exists(video_file) and os.path.exists(audio_file):
            editor = FootballVideoEditor()
            success = editor.process_video(video_file, audio_file)
            sys.exit(0 if success else 1)
        else:
            print("❌ One or both files not found")
            sys.exit(1)
    else:
        success = main()
        sys.exit(0 if success else 1)
