from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file, after_this_request
import os
import glob
from api_processor import process_audio

app = Flask(__name__)

# Set up signing for sessions
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page of the app with a form to form to submit text for processing into audio. When the form is submitted, the user is shown a message that the file is being processed.
    """
    voice_options = [
        'Alloy',
        'Echo',
        'Fable',
        'Onyx',
        'Nova',
        'Shimmer'
    ]
    if request.method == 'POST':
        output_file_name = request.form['output_file_name']
        session['output_file_name'] = output_file_name
        voice_selection = request.form['voice_selection'].lower()
        api_key = request.form['api_key']
        text_to_convert = request.form['text_to_convert']

        # Signal to the user that the file is being processed
        flash('Please wait, your file is being created.')

        # Call the function that processes the audio with threading to avoid freezing the Flask server
        from threading import Thread
        thread = Thread(target=process_audio_thread, args=(output_file_name, voice_selection, api_key, text_to_convert))
        thread.start()

        # Redirect to the same page which will display the flash message
        return redirect(url_for('index'))

    # If it's not a POST request, just render the page
    return render_template('index.html', voice_options=voice_options)


def process_audio_thread(output_file_name, voice_selection, api_key, text_to_convert):
    """
    Function that processes the audio with threading to avoid freezing the Flask server.
    Param str output_file_name: Name of the output file
    Param str voice_selection: Name of the voice to use
    Param str api_key: User's API key
    Param str text_to_convert: Text to convert to audio
    """
    process_result = process_audio(output_file_name, voice_selection, api_key, text_to_convert)

@app.route('/check-file-ready')
def check_file_ready():
    """
    Function that checks if the audio file is ready to be downloaded.
    Return json: Object with file status and file path
    """
    output_file_name = session.get('output_file_name')  # Use session to retrieve the file name
    if output_file_name:
        file_path = f'static/audio/{output_file_name}_full.mp3'
        file_ready = os.path.exists(file_path)
        return jsonify({'fileReady': file_ready, 'filePath': url_for('static', filename=f'audio/{output_file_name}_full.mp3')})
    else:
        # If we don't have an output_file_name, it's an error or the session has expired
        return jsonify({'fileReady': False, 'error': 'No output file name in session.'}), 400


@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.static_folder, 'audio', filename,'_full.mp3')
        # Register a function to run after the request is complete to delete the file
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
                app.logger.info(f'Successfully removed {file_path}')
            except Exception as error:
                app.logger.error(f'Error removing the file: {error}')
            return response
        # Send the file and allow it to be downloaded
        response = send_file(file_path, as_attachment=True)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    except FileNotFoundError:
        return jsonify(error='File not found.'), 404

def cleanup_old_files():
  """
  Function that deletes old files from the static/audio folder. The chunked files are deleted during the processing process. But full files are retained for a short-time to ensure that users can download the file.
  """
  
  # Set the path to the folder containing the files.
  directory = os.path.join(app.static_folder, 'audio')
  # Set the age threshold for deletion (e.g., 1 hour).
  cutoff_time = datetime.utcnow() - timedelta(hours=1)
  # Iterate over each file in the directory.
  for file_path in glob.glob(directory + '/*'):
      # Get the file's creation time.
      creation_time = datetime.utcfromtimestamp(os.path.getctime(file_path))
      # If the file is older than the cutoff time, delete it.
      if creation_time < cutoff_time:
          os.remove(file_path)
          print(f'Deleted {file_path}')
# Initialize the scheduler
scheduler = BackgroundScheduler()
# Schedule the `cleanup_old_files` function to run every hour.
scheduler.add_job(func=cleanup_old_files, trigger='interval', hours=1)
# Start the scheduler
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
