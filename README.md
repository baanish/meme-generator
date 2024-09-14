# Meme Generator
This is a Python script that generates a GIF from a YouTube video. It downloads the video, extracts the audio, transcribes the audio with OpenAI Whisper to generate subtitles, and then combines the video with the subtitles to create a sharable GIF.

## Requirements
- Python 3.x
- yt-dlp
- whisper-timestamped
- ffmpeg-python
- FFmpeg (command-line tool)

## Installation
1. Clone this repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure FFmpeg is installed on your system and accessible from the command line

## Usage
1. Run the script using:
   ```bash
   python generate_meme.py
   ```
2. Enter a YouTube link when prompted
3. Choose whether you want subtitles (y/n)
4. If you chose subtitles, enter the desired font size (default is 48)
5. Find the output GIF in the same directory as the script

## Features
- Downloads YouTube videos
- Extracts audio from the video
- Transcribes audio using OpenAI Whisper
- Generates subtitles with customizable font size
- Creates a GIF with or without subtitles
- Cleans up temporary files after processing

## License
This project is licensed under the MIT License. See the LICENSE file for details.
