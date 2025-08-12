#!/usr/bin/env python3
"""
Football AI Video Editor - Video Analysis Script
Analyze video properties and suggest optimal processing settings.
"""

import os
import sys
from pathlib import Path

# Dependency check
def check_dependencies():
    """Check if MoviePy is available"""
    try:
        import moviepy.editor
        return True
    except ImportError:
        print("❌ MoviePy is not installed!")
        print("\n🔧 To fix this:")
        print("1. Run: python scripts/install_requirements.py")
        print("2. Or manually: pip install moviepy imageio imageio-ffmpeg")
        print("3. Then run this script again")
        return False

if not check_dependencies():
    sys.exit(1)

from moviepy.editor import VideoFileClip

class VideoAnalyzer:
    def __init__(self):
        self.target_width = 608
        self.target_height = 1080
    
    def analyze_video(self, video_path):
        """Analyze video properties"""
        print(f"🔍 Analyzing video: {video_path}")
        print("-" * 50)
        
        try:
            video = VideoFileClip(video_path)
            
            # Basic properties
            width, height = video.size
            duration = video.duration
            fps = video.fps
            
            print(f"📐 Dimensions: {width} x {height}")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            print(f"🎞️  Frame rate: {fps:.2f} fps")
            print(f"📊 Total frames: {int(duration * fps)}")
            
            # Aspect ratio analysis
            aspect_ratio = width / height
            target_ratio = self.target_width / self.target_height
            
            print(f"📏 Current aspect ratio: {aspect_ratio:.3f} ({width}:{height})")
            print(f"🎯 Target aspect ratio: {target_ratio:.3f} ({self.target_width}:{self.target_height})")
            
            # Determine processing strategy
            if aspect_ratio > target_ratio:
                strategy = "CROP_SIDES"
                crop_amount = width - (height * target_ratio)
                print(f"📱 Strategy: Crop sides (remove {crop_amount:.0f}px width)")
            else:
                strategy = "CROP_TOP_BOTTOM"
                crop_amount = height - (width / target_ratio)
                print(f"📱 Strategy: Crop top/bottom (remove {crop_amount:.0f}px height)")
            
            # Audio analysis
            if video.audio:
                print(f"🎵 Audio: Present")
                print(f"🎵 Audio duration: {video.audio.duration:.2f} seconds")
            else:
                print(f"🔇 Audio: None")
            
            # File size
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            print(f"💾 File size: {file_size:.2f} MB")
            
            # Estimated output size
            pixel_reduction = (self.target_width * self.target_height) / (width * height)
            estimated_size = file_size * pixel_reduction
            print(f"📊 Estimated output size: {estimated_size:.2f} MB")
            
            video.close()
            
            return {
                'width': width,
                'height': height,
                'duration': duration,
                'fps': fps,
                'aspect_ratio': aspect_ratio,
                'strategy': strategy,
                'file_size_mb': file_size,
                'estimated_output_mb': estimated_size
            }
            
        except Exception as e:
            print(f"❌ Error analyzing video: {e}")
            return None
    
    def analyze_directory(self, directory_path):
        """Analyze all videos in a directory"""
        print(f"📁 Analyzing videos in: {directory_path}")
        print("=" * 60)
        
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
        video_files = []
        
        for file_path in Path(directory_path).iterdir():
            if file_path.suffix.lower() in video_extensions:
                video_files.append(file_path)
        
        if not video_files:
            print("❌ No video files found")
            return
        
        total_size = 0
        total_duration = 0
        analyses = []
        
        for video_file in video_files:
            analysis = self.analyze_video(str(video_file))
            if analysis:
                analyses.append(analysis)
                total_size += analysis['file_size_mb']
                total_duration += analysis['duration']
            print()  # Empty line between analyses
        
        # Summary
        print("📊 DIRECTORY SUMMARY")
        print("-" * 30)
        print(f"📹 Total videos: {len(analyses)}")
        print(f"⏱️  Total duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
        print(f"💾 Total size: {total_size:.2f} MB")
        
        if analyses:
            avg_duration = total_duration / len(analyses)
            estimated_output_size = sum(a['estimated_output_mb'] for a in analyses)
            print(f"📊 Average duration: {avg_duration:.2f} seconds")
            print(f"📊 Estimated total output size: {estimated_output_size:.2f} MB")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python video_analyzer.py <video_file_or_directory>")
        print("Examples:")
        print("  python scripts/video_analyzer.py video.mp4")
        print("  python scripts/video_analyzer.py ./videos/")
        return False
    
    path = sys.argv[1]
    
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return False
    
    analyzer = VideoAnalyzer()
    
    if os.path.isfile(path):
        # Analyze single file
        analysis = analyzer.analyze_video(path)
        return analysis is not None
    elif os.path.isdir(path):
        # Analyze directory
        analyzer.analyze_directory(path)
        return True
    else:
        print(f"❌ Invalid path: {path}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
