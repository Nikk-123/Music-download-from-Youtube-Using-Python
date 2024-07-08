from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import requests
import eyed3

def download_youtube_video_as_mp3(url, output_path):
    # Step 1: Download the YouTube video in the highest quality audio
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    downloaded_file = audio_stream.download(output_path=output_path)
    
    # Step 2: Convert the downloaded file to MP3
    mp4_file = downloaded_file
    mp3_file = downloaded_file.replace('.mp4', '.mp3').replace('.webm', '.mp3')
    
    audio_clip = AudioFileClip(mp4_file)
    audio_clip.write_audiofile(mp3_file)
    
    # Step 3: Add thumbnail (cover art) to the MP3 file
    thumbnail_url = yt.thumbnail_url
    if thumbnail_url:
        thumbnail_data = requests.get(thumbnail_url).content
        audiofile = eyed3.load(mp3_file)
        if audiofile.tag is None:
            audiofile.initTag()
        audiofile.tag.images.set(3, thumbnail_data, "image/jpeg", "Thumbnail")
        audiofile.tag.save()
    
    # Clean up: Delete the downloaded video file
    audio_clip.close()
    os.remove(mp4_file)

    return mp3_file

# Example usage
youtube_url = "https://www.youtube.com/watch?v=Qsn7w0WS7HQ"
output_path = "./"
mp3_file = download_youtube_video_as_mp3(youtube_url, output_path)
print(f"MP3 file saved at: {mp3_file}")
