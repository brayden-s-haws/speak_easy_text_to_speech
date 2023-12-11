import re
from user_config import text_to_convert

def remove_image_filenames(text):
  """
  Removes lines that contain image file names using regex. These are sometimes included in text when copying and pasting from a source that contains images
  
  param str text: text to be processed that may contain image file names
  return str: text with image file names removed
  """
  # Regex pattern to match entire lines containing image file names. This assumes the image file names are on a seperate line from the text. This may need refactor in the future to deal with cases where they are on the same line as the text.
  filename_pattern = re.compile(r'^.*\b\S+\.(?:png|jpg|jpeg|gif|JPG)\b.*$', re.MULTILINE)
  return filename_pattern.sub('', text)

def remove_emojis(text):
  """
  Removes emojis from text using regex. If these are not removed TTS will try to interpret them and read them.
  
  param str text: text to be processed that may contain emojis
  return str: text with emojis removed
  """
  # Regex pattern to match all emojis
  emoji_pattern = re.compile(
      "["
      "\U0001F600-\U0001F64F"  # emoticons
      "\U0001F300-\U0001F5FF"  # symbols & pictographs
      "\U0001F680-\U0001F6FF"  # transport & map symbols
      "\U0001F700-\U0001F77F"  # alchemical symbols
      "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
      "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
      "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
      "\U0001FA00-\U0001FA6F"  # Chess Symbols
      "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
      "\U00002702-\U000027B0"  # Dingbats
      "\U000024C2-\U0001F251"  # emoticons
      "]+", flags=re.UNICODE)

  return emoji_pattern.sub(r'', text)

def remove_paragraph_spaces(text):
  """
  Removes paragraph spaces from text using regex. Paragraph spaces are often included in text when copying and pasting. These are removed to make the string cleaner for TTS.
  
  param str text: text to be processed that may contain paragraph spaces
  return str: text with paragraph spaces removed
  """
  # First normalize different types of line breaks to just \n
  normalized_text = text.replace('\r\n', '\n').replace('\r', '\n')

  # Split the text by double newlines to separate paragraphs
  paragraphs = normalized_text.split('\n\n')

  # Trim spaces in each paragraph and replace internal newlines with a space
  paragraphs = [' '.join(para.split()) for para in paragraphs]

  # Join the paragraphs with a space to get the full cleaned text
  return ' '.join(paragraphs)


def split_text_into_chunks(text, chunk_size=4000):
  """
  Splits text into chunks of a given size. In this case we aim for chunks that are 4000 chartacters (the API limit is 4096 characters). However we first detect a space before chunking the text. This is to prevent TTS from splitting a word into two chunks. If the total text is less than 4000 characters, we do not chunk the text but do place it in the dictionary for processing downstream

  param str text: text to be processed into chunks
  param int chunk_size: size of chunks to be created
  return dict: dictionary of chunks with number, incrementing keys and corresponding chunks as values
  """
  chunks = {}
  chunk_number = 1
  while text:
      # Find nearest space before the chunk_size to avoid splitting words
      if len(text) > chunk_size:
          split_index = text.rfind(' ', 0, chunk_size)
          if split_index == -1:  # In case there's no space, fall back to the original chunk_size
              split_index = chunk_size
      else:
          split_index = len(text)
      # Slice the text to get the current chunk and store it in the dictionary
      chunks[chunk_number] = text[:split_index].strip()
      # Remove the chunk from the text
      text = text[split_index:].lstrip()
      # Increment for the next chunk number
      chunk_number += 1
  return chunks

input_text = text_to_convert
input_text = remove_emojis(input_text)
input_text = remove_image_filenames(input_text)
input_text = remove_paragraph_spaces(input_text)
text_dict = split_text_into_chunks(input_text)
