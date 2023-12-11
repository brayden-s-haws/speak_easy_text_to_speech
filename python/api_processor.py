import os
import subprocess
from pathlib import Path
from openai import OpenAI
from text_processor import text_dict
from user_config import voice_selection, output_file_name
client = OpenAI()

def concatenate_mp3_files(output_file_name, directory='.'):
  """
  Concatenates all generated mp3 files into a single file

  param str output_file_name: Name of the output file selected by user
  param str directory: Directory of the mp3 files
  return: mp3 file
  """
  # Get all mp3 files sorted numerically by the number in the filename
  # TODO: Update this to support more than 9 files
  mp3_files = sorted(Path(directory).glob(f'{output_file_name}[0-9]*.mp3'),
                     key=lambda x: int(x.stem.replace(output_file_name, '')))
  # Create a temporary file list
  with open('file_list.txt', 'w') as f:
      for mp3_file in mp3_files:
          f.write(f"file '{mp3_file}'\n")
  # Use ffmpeg to concatenate the MP3 files
  subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', 
                  '-c', 'copy', f'{output_file_name}_full.mp3'])
  # Remove the temporary file list
  os.remove('file_list.txt')



for k, v in text_dict.items():
  # Interate through each text chunk and generate an mp3 file
  speech_file_path = Path(__file__).parent / (output_file_name + str(k) + '.mp3')
  response = client.audio.speech.create(
    model= 'tts-1-hd', # tts-1 for faster processing speed, tts-1-hd for higher quality
    voice= voice_selection, #choose from one of six voices
    input= v
  )

  response.stream_to_file(speech_file_path)

output_file_name = output_file_name
concatenate_mp3_files(output_file_name) #concatenate all mp3 files into a single file

print()
print('Your File is Ready')
