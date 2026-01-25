import yt_dlp
import whisper_timestamped as whisper
import ffmpeg
import subprocess
from datetime import timedelta
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a meme GIF from a YouTube video with optional subtitles.")
    parser.add_argument("url", nargs='?', help="YouTube video URL. If not provided, script will prompt for it.")
    parser.add_argument("--subtitle", choices=['y', 'n'], help="Add subtitles? (y/n). If not provided, script will prompt.")
    parser.add_argument("--fontsize", type=str, help="Subtitle font size. If not provided, script will prompt if subtitles are 'y'.")

    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = input("Enter a youtube link: ")

    if args.subtitle:
        subtitle = args.subtitle
    else:
        subtitle = input("Do you want subtitles? (y/n): ") or 'y'

    if subtitle == 'y':
        if args.fontsize:
            fontsize = args.fontsize
        else:
            fontsize = input("What font size do you want? (default 48): ") or '48'
    else:
        fontsize = '48' # Default, not used if subtitle is 'n'


    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"An error occurred during video download: {str(e)}")
        sys.exit(1)

    # extract audio
    try:
        subprocess.run(['ffmpeg', '-i', 'video.mp4', '-q:a', '0', '-map', 'a', 'audio.mp3', '-y'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during audio extraction: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("ffmpeg not found. Please ensure ffmpeg is installed and in your PATH.")
        sys.exit(1)


    # transcribe audio
    try:
        model = whisper.load_model("base")
        result = whisper.transcribe(model, "audio.mp3")
        segments = result['segments']
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        # Depending on the desired behavior, you might want to exit here or continue without subtitles
        # For now, let's assume if transcription fails, we can't proceed with subtitles.
        if subtitle == 'y':
            print("Cannot generate subtitles due to transcription error.")
            sys.exit(1)
        segments = [] # Ensure segments is defined even if transcription fails and subtitles are off

    if subtitle == 'y':
        # output subtitles to file
        with open('subtitles.srt', 'w') as f:
            segment_id = 1
            for segment_data in segments:
                start_time = str(0)+str(timedelta(seconds=int(segment_data['start'])))+',000'
                end_time = str(0)+str(timedelta(seconds=int(segment_data['end'])))+',000'
                text = segment_data['text'].strip()
                
                # Split text into chunks of max 2 lines
                lines = text.split('\n')
                for i in range(0, len(lines), 2):
                    chunk = '\n'.join(lines[i:i+2])
                    subtitle_entry = f"{segment_id}\n{start_time} --> {end_time}\n{chunk}\n\n"
                    f.write(subtitle_entry)
                    segment_id += 1
            # No f.close() needed with 'with open(...)'

        # Set up the subtitle stream
        try:
            video_input = ffmpeg.input('video.mp4')
            subtitled_stream = video_input.filter('subtitles', 'subtitles.srt', force_style=f'FontName=Impact,FontSize={fontsize}')
            # output as a GIF
            ffmpeg.run(ffmpeg.output(subtitled_stream, 'output.gif'), overwrite_output=True)
        except ffmpeg.Error as e:
            print(f"Error during GIF generation with subtitles: {e.stderr.decode('utf8') if e.stderr else e}")
            sys.exit(1)
        
    else:
        # output as a GIF
        try:
            video_input = ffmpeg.input('video.mp4')
            ffmpeg.run(ffmpeg.output(video_input, 'output.gif'), overwrite_output=True)
        except ffmpeg.Error as e:
            print(f"Error during GIF generation without subtitles: {e.stderr.decode('utf8') if e.stderr else e}")
            sys.exit(1)


    # delete video, subtitles, and audio files
    if os.path.exists('video.mp4'):
        os.remove('video.mp4')
    if os.path.exists('audio.mp3'):
        os.remove('audio.mp3')
    if os.path.exists('subtitles.srt'):
        os.remove('subtitles.srt')

if __name__ == "__main__":
    main()
