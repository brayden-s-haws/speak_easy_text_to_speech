import os
import subprocess
import logging
from pathlib import Path
from openai import OpenAI
from text_processor import (remove_emojis, remove_image_filenames, remove_paragraph_spaces, split_text_into_chunks)
import re

# Add logging to track basic application operations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def concatenate_mp3_files(output_filename, mp3_files):
    """
    Concatenates a list of mp3 files into a single file.
    param str output_filename: Name of the output mp3 file
    param list mp3_files: List of mp3 files to concatenate
    return mp3_file: Name of the concatenated mp3 file
    """
    concat_file = f'static/audio/{output_filename}_full.mp3'
    with open('file_list.txt', 'w') as f:
        for mp3_file in mp3_files:
            f.write(f"file '{mp3_file}'\n")
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', 
                    '-c', 'copy', concat_file])
    os.remove('file_list.txt')
    logging.info(f"Concatenated audio file created at {concat_file}.")
    return concat_file


def process_audio(output_file_name, voice_selection, api_key, text_to_convert):
    """
    Takes files through a number of steps to clean them up removing emojis, images, and paragraph spaces. Files are then chunked into chunks of length 4000 characters. Each chunk is then processed through OpenAI's tts model. Finally, the chunks are concatenated into a single mp3 file. The chunk files are then deleted to keep environment clean.
    param str output_file_name: Name of the output mp3 file
    param str voice_selection: Name of the voice to use for the mp3 files
    param str api_key: OpenAI API key
    param str text_to_convert: Text to convert to mp3
    return mp3_file: Name of the concatenated mp3 file
    """
    try:
        # Adding detailed logging here in the case that any step fails
        logging.info('Starting audio processing.')
        
        logging.info('Preprocessing text: removing image filenames.')
        processed_text = remove_image_filenames(text_to_convert)
        logging.info('Image filenames removed.')

        logging.info('Preprocessing text: removing emojis.')
        processed_text = remove_emojis(processed_text)
        logging.info('Emojis removed.')

        logging.info('Preprocessing text: removing paragraph spaces.')
        processed_text = remove_paragraph_spaces(processed_text)
        logging.info('Paragraph spaces removed.')

        logging.info('Splitting text into chunks.')
        text_dict = split_text_into_chunks(processed_text)
        logging.info(f'{len(text_dict)} chunks have been created for processing.')

        client = OpenAI(api_key=api_key)
        audio_files = []

        for k, v in text_dict.items():
            logging.info(f'Requesting TTS for text chunk #{k}.')
            speech_file_path = Path('static/audio/') / (output_file_name + str(k) + '.mp3')
            response = client.audio.speech.create(
                model='tts-1-hd',
                voice=voice_selection,
                input=v
            )
            logging.info(f'Received TTS response for chunk #{k}.')
            response.stream_to_file(str(speech_file_path))
            audio_files.append(speech_file_path)
      
        full_audio_path = concatenate_mp3_files(output_file_name, audio_files)
        logging.info(f'Audio processing complete, full audio available at: {full_audio_path}.')
        # This removes the individual audio files after concatenation
        for file_path in audio_files:
            try:
                file_path.unlink(missing_ok=True)
                logging.info(f'Temporary audio file {file_path} removed.')
            except Exception as e:
                logging.error(f'Failed to remove temporary audio file {file_path}: {e}')

        return True
    except Exception as e:
        logging.error(f'An error occurred during audio processing: {e}')
        return False
