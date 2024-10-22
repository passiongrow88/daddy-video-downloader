from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os
import time

app = Flask(__name__)

# Create a directory to store downloads temporarily
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    # Detect user-agent for platform-specific instructions
    user_agent = request.headers.get('User-Agent')

    if 'Android' in user_agent:
        platform_message = "<p>Downloading on Android: Just tap the download link after the process is complete.</p>"
    elif 'iPhone' in user_agent or 'iPad' in user_agent:
        platform_message = "<p>Downloading on iOS: Long-press the download link and choose 'Download Linked File' to save the video.</p>"
    else:
        platform_message = "<p>Downloading anytime & anywhere.</p>"

    # Render the index.html template and pass the platform_message variable
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

    # Set download options for 1080p max resolution
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # Limit video to 1080p max
        'n_threads': 4,  # Parallel download with 4 threads
        'verbose': True,  # Enable verbose output to monitor download speed
        'cookiefile': 'cookies.txt'  # Use a cookie file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)

            # Add a delay to reduce CPU spikes after the download
            time.sleep(5)  # Pauses the program for 5 seconds

            # After downloading, show a link to download the file manually
            return render_template('download_complete.html', file_link=url_for('download_file', file=file_name))

    except Exception as e:
        return f"Error downloading video: {str(e)}"

# Serve the file when the user clicks the download link
@app.route('/download_file')
def download_file():
    file_name = request.args.get('file')

    if not file_name or not os.path.exists(file_name):
        return "Error: File not found"

    # Serve the file to the user
    response = send_file(file_name, as_attachment=True)

    # After sending the file, delete it
    try:
        os.remove(file_name)
    except Exception as e:
        print(f"Error deleting file {file_name}: {str(e)}")

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
