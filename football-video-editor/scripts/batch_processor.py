#!/usr/bin/env python3
"""
Football AI Video Editor - Batch Processing Script
Process multiple video files with the same audio track.
"""

import os
import sys
from pathlib import Path

# Check for dependencies before importing
try:
    from football_video_editor import FootballVideoEditor
except ImportError as e:
    print("❌ Required dependencies are not installed!")
    print(f"Error: {e}")
    print("\n📋 To fix this issue:")
    print("1. Run: python scripts/troubleshoot.py")
    print("2. Or install manually: pip install moviepy imageio imageio-ffmpeg")
    print("3. Then run this script again")
    sys.exit(1)

def batch_process_videos(video_directory, audio_file, output_directory="output"):
    """Process multiple videos in a directory with the same audio"""
    
    editor = FootballVideoEditor()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Supported video extensions
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    
    # Find all video files
    video_files = []
    for file_path in Path(video_directory).iterdir():
        if file_path.suffix.lower() in video_extensions:
            video_files.append(file_path)
    
    if not video_files:
        print(f"❌ No video files found in {video_directory}")
        return False
    
    print(f"🎬 Found {len(video_files)} video files to process")
    
    successful_processes = 0
    failed_processes = 0
    
    for i, video_path in enumerate(video_files, 1):
        print(f"\n📹 Processing {i}/{len(video_files)}: {video_path.name}")
        
        # Generate output filename
        output_filename = f"{video_path.stem}_vertical{video_path.suffix}"
        output_path = os.path.join(output_directory, output_filename)
        
        try:
            success = editor.process_video(str(video_path), audio_file, output_path)
            if success:
                successful_processes += 1
                print(f"✅ Successfully processed: {output_filename}")
            else:
                failed_processes += 1
                print(f"❌ Failed to process: {video_path.name}")
        
        except Exception as e:
            failed_processes += 1
            print(f"❌ Error processing {video_path.name}: {e}")
    
    print(f"\n📊 BATCH PROCESSING RESULTS")
    print(f"✅ Successful: {successful_processes}")
    print(f"❌ Failed: {failed_processes}")
    print(f"📁 Output directory: {output_directory}")
    
    return successful_processes > 0

def main():
    """Main function for batch processing"""
    if len(sys.argv) < 3:
        print("Usage: python batch_processor.py <video_directory> <audio_file> [output_directory]")
        print("Example: python batch_processor.py ./videos isak_voice.mp3 ./output")
        return False
    
    video_directory = sys.argv[1]
    audio_file = sys.argv[2]
    output_directory = sys.argv[3] if len(sys.argv) > 3 else "output"
    
    if not os.path.exists(video_directory):
        print(f"❌ Video directory not found: {video_directory}")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    return batch_process_videos(video_directory, audio_file, output_directory)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
