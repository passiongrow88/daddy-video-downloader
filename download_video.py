from flask import Flask, render_template, request, send_file, url_for
import yt_dlp
import os
import time

app = Flask(__name__)

# Ensure downloads directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    platform_message = "<p>Downloading anytime & anywhere.</p>"
    if 'Android' in user_agent:
        platform_message = "<p>Downloading on Android: Just tap the download link after the process is complete.</p>"
    elif 'iPhone' in user_agent or 'iPad' in user_agent:
        platform_message = "<p>Downloading on iOS: Long-press the download link and choose 'Download Linked File' to save the video.</p>"

    return render_template('index.html', platform_message=platform_message)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']

    if not video_url:
        return '''
        <div class="container mt-5">
            <div class="alert alert-danger text-center" role="alert">
                Error: No URL provided. Please enter a valid video URL.
            </div>
            <a href="/" class="btn btn-primary">Go Back</a>
        </div>
        '''

    # Set yt-dlp options, including your residential IP as proxy
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies.txt',
        'proxy': 'http://121.121.48.140',  # Replace with your actual IP if it changes
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            time.sleep(5)  # Delay to reduce CPU spikes

            return render_template('download_complete.html', file_link=url_for('download_file', file=file_name))

    except Exception as e:
        return f"Error downloading video: {str(e)}"

@app.route('/download_file')
def download_file():
    file_name = request.args.get('file')

    if not file_name or not os.path.exists(file_name):
        return "Error: File not found"

    response = send_file(file_name, as_attachment=True)
    try:
        os.remove(file_name)
    except Exception as e:
        print(f"Error deleting file {file_name}: {str(e)}")

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
