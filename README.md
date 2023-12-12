## Description
SpeakEasy is a straigtforward and easy to use text-to-speech tool. It was born out of my desire to convert some of my blog posts into audio format. It was then expanded to support nearly any body of text. It works in a transactional manner, there are no accounts or subscriptions. Users fill in a few details and SpeakEasy does the heavy lifting to process their text into audio using the OpenAI API. The code is available in both python and flask versions, depending on whether or not a front end is needed. 

SpeakEasy uses the hd version of the text-to-speech api which leads to high quality outputs, you can hear some sample outputs [here](https://haws.notion.site/Audio-Blog-Posts-26d29fb160d1421cb7bf4bf252589347).

You can watch a demo of the web app version below and give it a try for yourself [here](https://speak-easy.replit.app).

https://github.com/brayden-s-haws/speak_easy_text_to_speech/assets/58832489/6197b5a9-31e7-403d-8a2d-944034cfba12

## How It Works
SpeakEasy takes in a handful of inputs from the user and uses those to turn the text they submit into an mp3 audio file. This diagram shows the basic flow:
![CleanShot Freeform-2023-12-11](https://github.com/brayden-s-haws/speak_easy_text_to_speech/assets/58832489/6ecb436d-03ce-4689-ba3c-54cde170f403)

- User Form - The user fills out the web form to start the process:
  - Details in the form, including the API key are only stored during the session. Once user navigates away from the page all details are deleted.
- Text Processing - The text submitted by the user is processed in a few ways:
  - Emojis and image references are removed. These can often be included in text when copying and pasting from a source. But we do not want the AI voice reading them outloud.
  - Paragraph spacing ins removed. The API expects a single string so cleaning up the spacing makes the text easier to handle as we prep it to be sent.
  - Text is chunked and stored in a list of text chunks. The API character limit is 4096 characters. Text is broken into chunks of approximately 4000 characters to avoid this limit. Chunking is done only on spaces in the text so that a word is not split and sent in two seperate chunks.
- Audio Processing - The prepared text is sent to the OpenAI TTS API for processing into mp3 format
  - Each text chunk is sent seperately and the returned MP3 file is stored.
  - Once all chunks have been processed the files are concatenated and the individual MP3 files are deleted.
  - The final file is made available to users to download through a link in the UI.

## Files

#### Flask:

- **app.py**: This is the main file of the flask app. It launches the web app, displays the web form for users, checks file processing status, and presents users with the file download link.
- **text_processor.py**: This file contains all the functions for cleaning and preparing text prior to the API sends.
- **api_processor.py**: This file manages the sending of each text chunk for processing by the API. It also concatenates the files and cleans up the individual files.
- **index.html**: This file contains all the HTML, CSS, and Javascript required for the frontend. It contains the various display states of the app. Additonally the contexts of the "How it works" and "FAQ" sections are stored here. This file is stored in the templates folder. (Apologies to anyone who has to look at this, frontend is not my strong suit).

In addition to these files the Flask version of the code expects there to be a logo image file stored at static > images. Generated audio files will be stored at static > audio

#### Python:
- **user_config.py**: This file contains the required details for converting text to audio. In this version the user enters the needed info into the console and triggers the processing through a key word.
- **text_processpr**: This file manages all the functions for cleaning and preparing text prior to the API sends. It outputs a dictionary of text chunks that are passed to the API.
- **api_processor**: This file manages the sending of each text chunk for processing by the API. It also concatenates the files and cleans up the individual files.

## Setup


## Acknowledgements
