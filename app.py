from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Enable CORS if frontend runs separately

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_download_link', methods=['POST'])
def get_download_link():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'quiet': True,
        'format': '18/best',
        'skip_download': True,
        'forceurl': True,
        'forcejson': True,
        'cookiefile': 'cookies.txt' 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info['url']
            title = info.get('title', 'Video')
            return jsonify({'url': download_url, 'title': title})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
