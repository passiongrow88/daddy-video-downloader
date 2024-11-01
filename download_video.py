from flask import Flask, render_template, request, send_file, url_for, redirect
import yt_dlp
import os

app = Flask(__name__)

# Create a directory to store downloads temporarily
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    return '''
    <form action="/download" method="post">
        <label for="url">Enter YouTube Video URL:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Download Video</button>
    </form>
    '''

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']

    if not video_url:
        return "Error: No URL provided. Please enter a valid video URL."

    # Set download options for 1080p max resolution and MP4 format
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.mp4',  # Save as MP4
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies.txt'  # Ensure this file is in the same directory as this script
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)

        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return f"Error downloading video: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
