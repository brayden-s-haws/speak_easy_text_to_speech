import getpass

def get_multiline_input(prompt="Please paste your text here (Type 'END' to finish): "):
  """
  Prompts the user to paste in all the text they wish to process. The user must type 'END' to indicate they are done inputing text.
  param str prompt: The prompt to display to the user.
  return str: The text the user entered.
  """
  print(prompt)
  lines = []
  while True:
      line = input()
      if line == 'END':  # User types 'END' to indicate they are finished entering text
          break
      lines.append(line)
  return "\n".join(lines)

output_file_name = input('What would you like to name your mp3 file? ') # User enters the name of what they would like the output file to be named.
voice_selection = input('What voice would you like to use? ') # User enters the name of the voice they would like to use. This is limited to the voice options from OpenAI
api_key = getpass.getpass('Please enter your api key: ') # User enters their OpenAI api key
text_to_convert = get_multiline_input() # User enters the text they wish to convert.
