import yt_dlp
import os

# Request the video URL from the user
video_url = input("Enter the YouTube video URL: ")

# Ensure downloads directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Set yt-dlp options
ydl_opts = {
    'outtmpl': 'downloads/%(title)s.mp4',  # Set output to .mp4
    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # Download up to 1080p
    'n_threads': 4,
    'verbose': True,
    'cookiefile': 'cookies.txt',  # Ensure this file is in the same directory as this script
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate'
    },
    'merge_output_format': 'mp4'  # Ensure merging into .mp4 format
}

# Download the video
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print("Download completed successfully.")
except Exception as e:
    print("An error occurred during the download process.")
    print("Error output:", str(e))
