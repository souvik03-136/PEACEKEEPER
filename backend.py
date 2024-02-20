from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from summarize import summarize_pdf
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Define the uploads directory path
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

@app.route('/')
def index():
    print("IM UNDDER INDEX FUCNTION")
    return render_template('index.html')

def process_file(file):
    print("FILE IS UPLOADED")
    try:
        # Create the 'uploads' directory if it doesn't exist
        if not os.path.exists(UPLOADS_DIR):
            app.logger.debug("Creating uploads directory...")
            os.makedirs(UPLOADS_DIR)
            app.logger.debug("Uploads directory created successfully.")

        # Save the uploaded file to a temporary location
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        file_path = file_path.replace('\\', '\\\\')  # Replace single backslashes with double backslashes
        file.save(file_path)

        # Pass the file path to summarize_pdf function
        summary_text = summarize_pdf(file_path)

        # Print the summary text for debugging
        app.logger.debug("Summary text:", summary_text)

        # Emit the summary text to the frontend
        socketio.emit('summary_text', {'text': summary_text})

        # Remove the temporary file
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
    print("SERVER START")  # Print "SERVER START" when the script is executed
    socketio.run(app, debug=True)
