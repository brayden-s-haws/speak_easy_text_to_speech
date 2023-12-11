## Description
SpeakEasy is a straigtforward and easy to use text-to-speech tool. It was born out of my desire to convert some of my blog posts into audio format. It was then expanded to support nearly any body of text. It works in a transactional manner, there are no accounts or subscriptions. Users fill in a few details and SpeakEasy does the heavy lifting to process their text into audio using the OpenAI API. The code is available in both python and flask versions, depending on whether or not a front end is needed. 

SpeakEasy uses the hd version of the text-to-speech api which leads to high quality outputs, you can hear some sample outputs [here](https://haws.notion.site/Audio-Blog-Posts-26d29fb160d1421cb7bf4bf252589347).

You can watch a demo of the web app version below and give it a try for yourself [here](https://speak-easy.replit.app).
https://github.com/brayden-s-haws/speak_easy_text_to_speech/assets/58832489/6197b5a9-31e7-403d-8a2d-944034cfba12

## How It Works
SpeakEasy takes in a handful of inputs from user and uses those to turn the text they submit into an mp3 audio file. This diagram shows the basic flow:
![CleanShot Freeform-2023-12-11](https://github.com/brayden-s-haws/speak_easy_text_to_speech/assets/58832489/6ecb436d-03ce-4689-ba3c-54cde170f403)

- User Form:
-   Details in the form, including the API key are only stored during the session. Once user navigates away from the page all details are deleted.
- 



## Files

- **file_name**: 

## Setup


## Acknowledgements
