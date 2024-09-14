import yt_dlp
import whisper_timestamped as whisper
import ffmpeg
import subprocess
from datetime import timedelta
import os
import sys

# save video as mp4
url = input("Enter a youtube link: ")
subtitle = input("Do you want subtitles? (y/n): ") or 'y'
if subtitle == 'y':
    fontsize = input("What font size do you want? (default 48): ") or '48'

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': 'video.%(ext)s'
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(1)

# extract audio
subprocess.run(['ffmpeg', '-i', 'video.mp4', '-q:a', '0', '-map', 'a', 'audio.mp3'], check=True)

# transcribe audio
model = whisper.load_model("base")
result = whisper.transcribe(model, "audio.mp3")
segments = result['segments']

if subtitle == 'y':
    # output subtitles to file
    with open('subtitles.srt', 'w') as f:
        segment_id = 1
        for segment in segments:
            start_time = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            end_time = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text'].strip()
            
            # Split text into chunks of max 2 lines
            lines = text.split('\n')
            for i in range(0, len(lines), 2):
                chunk = '\n'.join(lines[i:i+2])
                subtitle = f"{segment_id}\n{start_time} --> {end_time}\n{chunk}\n\n"
                f.write(subtitle)
                segment_id += 1

        f.close()

    # Set up the subtitle stream

    subtitled = ffmpeg.input('video.mp4').filter('subtitles', 'subtitles.srt', force_style=f'FontName=Impact,FontSize={fontsize}')

    # output as a GIF
    ffmpeg.run(ffmpeg.output(subtitled, 'output.gif'), overwrite_output=True)
    
else:
    # output as a GIF
    ffmpeg.run(ffmpeg.output(ffmpeg.input('video.mp4'), 'output.gif'), overwrite_output=True)

# delete video, subtitles, and audio files
os.remove('video.mp4')
os.remove('audio.mp3')
if os.path.exists('subtitles.srt'):
    os.remove('subtitles.srt')
