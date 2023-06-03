from pytube import YouTube
import whisper
import ffmpeg
from datetime import timedelta
import os

# save video as mp4
url = input("Enter a youtube link: ")
subtitle = input("Do you want subtitles? (y/n): ") or 'y'
if subtitle == 'y':
    fontsize = input("What font size do you want? (default 48): ") or '48'
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()
stream.download('.', 'video.mp4')

# extract audio
ffmpeg.run(ffmpeg.output(ffmpeg.input('video.mp4').audio, 'audio.mp3'), overwrite_output=True)

# transcribe audio
segments = whisper.load_model("base").transcribe("audio.mp3")['segments']

if subtitle == 'y':
    # output subtitles to file
    # from https://github.com/openai/whisper/discussions/98#discussioncomment-3725983
    with open('subtitles.srt', 'w') as f:
        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

            f.write(segment)
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
if subtitle == 'y':
    os.remove('subtitles.srt')
