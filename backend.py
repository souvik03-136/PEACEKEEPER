from flask import Flask, render_template, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from summarize import summarize_pdf
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Define the uploads directory path
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOADS_DIR, filename)
    file.save(file_path)

    # Extract language from the request
    language = request.form.get('language')

    # Call process_file function with the file path and language
    process_file(file_path, language)
    return 'File uploaded successfully'


def process_file(file_path, language):
    try:
        # Pass the file path and language to summarize_pdf function
        summary_text = summarize_pdf(file_path, language)

        # Emit the summary text to the frontend
        socketio.emit('summary_text', {'text': summary_text})

        os.remove(file_path)

    except Exception as e:
        app.logger.error("Error:", e)  # Log any errors that occur
        return "An error occurred while processing the file."


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
