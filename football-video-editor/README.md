# Football AI Video Editor - Simple Version

## Quick Start

### Windows:
\`\`\`
run.bat
\`\`\`

### Linux/Mac:
\`\`\`
chmod +x run.sh
./run.sh
\`\`\`

### Manual Steps:
\`\`\`
1. python simple_installer.py
2. python test_simple.py  
3. python create_sample_files.py
4. python simple_editor.py sample_video.mp4 sample_audio.mp3
\`\`\`

## Usage

With your own files:
\`\`\`
python simple_editor.py your_video.mp4 your_audio.mp3
\`\`\`

## What it does:
- Resizes video to 608x1080 (vertical)
- Syncs audio to video length
- Exports as MP4 with H.264/AAC

## Requirements:
- Python 3.7+
- moviepy
- imageio
- imageio-ffmpeg
