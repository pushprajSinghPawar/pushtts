from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)

# Serve static files with cache-control headers set to no-cache
@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, cache_timeout=0)

@app.route('/')
def home():
    return render_template('index.html', audio_file=None)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    text = request.form.get('txt', '').strip()
    if text:
        var = gTTS(text=text, lang="hi")
        audio_filename = "eng.mp3"  # Same filename every time
        audio_file_path = os.path.join("static", audio_filename)

        # Delete the old file if it exists
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

        var.save(audio_file_path)
        return render_template('answer.html', audio_file=audio_filename, text=text)
    return render_template('answer.html', audio_file=None, text='')

if __name__ == "__main__":
    app = Flask(__name__, static_url_path='/static')
    app.run(debug=True)
