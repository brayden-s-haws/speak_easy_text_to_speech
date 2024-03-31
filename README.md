## Description
SpeakEasy is a straightforward and easy-to-use text-to-speech tool. It was born out of my desire to convert some of my blog posts into audio format. It was then expanded to support nearly any body of text. It works in a transactional manner, there are no accounts or subscriptions. Users fill in a few details and SpeakEasy does the heavy lifting to process their text into audio using the OpenAI API. The code is available in both Python and Flask versions, depending on whether or not a front end is needed. 

SpeakEasy uses the HD version of the text-to-speech API which leads to high-quality outputs, you can hear some sample outputs [here](https://haws.notion.site/Audio-Blog-Posts-26d29fb160d1421cb7bf4bf252589347).

You can watch a demo of the web app version below and give it a try for yourself [here](https://speak-easy.replit.app).

https://github.com/brayden-s-haws/speak_easy_text_to_speech/assets/58832489/6197b5a9-31e7-403d-8a2d-944034cfba12

## How It Works
SpeakEasy takes in a handful of inputs from the user and uses those to turn the text they submit into an mp3 audio file. This diagram shows the basic flow:
![CleanShot Freeform-2023-12-11](https://github.com/brayden-s-haws/speak_easy_text_to_speech/assets/58832489/6ecb436d-03ce-4689-ba3c-54cde170f403)

- User Form - The user fills out the web form to start the process:
  - Details in the form, including the API key are only stored during the session. Once the user navigates away from the page all details are deleted.
- Text Processing - The text submitted by the user is processed in a few ways:
  - Emojis and image references are removed. These can often be included in text when copying and pasting from a source. But we do not want the AI voice reading them out loud.
  - Paragraph spacing is removed. The API expects a single string so cleaning up the spacing makes the text easier to handle as we prep it to be sent.
  - Text is chunked and stored in a list of text chunks. The API character limit is 4096 characters. Text is broken into chunks of approximately 4000 characters to avoid this limit. Chunking is done only on spaces in the text so that a word is not split and sent in two separate chunks.
- Audio Processing - The prepared text is sent to the OpenAI TTS API for processing into mp3 format
  - Each text chunk is sent separately and the returned MP3 file is stored.
  - Once all chunks have been processed the files are concatenated and the individual MP3 files are deleted.
  - The final file is made available to users to download through a link in the UI.

```Mermaid
graph TD
  A[user_config.py] --> B{User Input}
  B --> C[output_file_name]
  B --> D[voice_selection]
  B --> E[api_key]
  B --> F[text_to_convert]
  
  F --> G[text_processor.py]
  G --> H[remove_emojis]
  G --> I[remove_image_filenames]
  G --> J[remove_paragraph_spaces]
  G --> K[split_text_into_chunks]
  K --> L[text_dict]
  
  L --> M[api_processor.py]
  M --> N{Iterate through text_dict}
  N --> O[Generate MP3 for each chunk]
  O --> P[Concatenate MP3 files]
  P --> Q[output_file_name_full.mp3]
```

## Files

#### Flask:

- **app.py**: This is the main file of the Flask app. It launches the web app, displays the web form for users, checks file processing status, and presents users with the file download link.
- **text_processor.py**: This file contains all the functions for cleaning and preparing text before the API sends.
- **api_processor.py**: This file manages the sending of each text chunk for processing by the API. It also concatenates the files and cleans up the individual files.
- **index.html**: This file contains all the HTML, CSS, and Javascript required for the front end. It contains the various display states of the app. Additionally, the contexts of the "How it works" and "FAQ" sections are stored here. This file is stored in the templates folder. (Apologies to anyone who has to look at this, frontend is not my strong suit).

In addition to these files, the Flask version of the code expects there to be a logo image file stored at static > images. Generated audio files will be stored at static > audio

#### Python:
- **user_config.py**: This file contains the required details for converting text to audio. In this version, the user enters the needed info into the console and triggers the processing through a keyword.
- **text_processpr**: This file manages all the functions for cleaning and preparing text before the API sends. It outputs a dictionary of text chunks that are passed to the API.
- **api_processor**: This file manages the sending of each text chunk for processing by the API. It also concatenates the files and cleans up the individual files.

## Setup
The compute demands for this are low since it is just some simple data cleaning and then sending to an API to do the heavy lifting. I deployed the Flask version of this on Replit on their smallest machine size and added some autoscaling backup, in case there is a lot of web traffic. If you don't require a front-end or web app you should be able to run the Python version locally on almost any machine. This set of commands will install all the required packages: `pip install Flask APScheduler requests openai ffmpeg-python`.

## Acknowledgements
Huge credit goes to [Ryan Jenson](https://github.com/rwjenson) for designing the entire UI. Without him, the Flask version wouldn't exist and we would all be running the Python version locally.
