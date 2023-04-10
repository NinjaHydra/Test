import os
import youtube_dl

# Set up the options for youtube-dl
ydl_opts = {
    'outtmpl': '%(playlist_index)s - %(title)s.%(ext)s',
    'quiet': False,
    'no_color': True,
}

# Define the function for downloading a video
def download_video(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Define the function for downloading a playlist
def download_playlist(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Define the function for resuming a download
def resume_download():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl._downloader.params['continuedl'] = True

# Define the function for pausing a download
def pause_download():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl._downloader.pause()

# Define the function for choosing the video or audio quality
def choose_quality():
    quality = input("Enter 'v' for video or 'a' for audio: ")
    if quality == 'v':
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    elif quality == 'a':
        ydl_opts['format'] = 'bestaudio/best'
    else:
        print("Invalid input, defaulting to audio")
        ydl_opts['format'] = 'bestaudio/best'

# Define the function for adding number prefixes to playlist videos
def add_prefix():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(ydl_opts['url'], download=False)
        prefix = input("Enter prefix for playlist videos (default is blank): ")
        for i, entry in enumerate(playlist_info['entries'], start=1):
            entry['title'] = f"{prefix}{i} - {entry['title']}"
            ydl.process_info(entry)

# Get the user's input for the video or playlist URL
url = input("Enter the YouTube video or playlist URL: ")

# Determine whether the input is a video or playlist and call the appropriate function
if 'list=' in url:
    ydl_opts['extract_flat'] = True
    download_playlist(url)
else:
    download_video(url)

# Ask the user if they want to add a prefix to the playlist videos
add_prefix_input = input("Do you want to add a number prefix to playlist videos? (y/n): ")
if add_prefix_input.lower() == 'y':
    add_prefix()

# Ask the user if they want to choose the quality
choose_quality_input = input("Do you want to choose the video or audio quality? (y/n): ")
if choose_quality_input.lower() == 'y':
    choose_quality()

# Ask the user if they want to pause or resume the download
while True:
    pause_resume_input = input("Enter 'p' to pause, 'r' to resume, or 'q' to quit: ")
    if pause_resume_input == 'p':
        pause_download()
    elif pause_resume_input == 'r':
        resume_download()
    elif pause_resume_input == 'q':
        break
    else:
        print("Invalid input, please try again")
