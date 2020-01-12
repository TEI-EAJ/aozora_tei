from bs4 import BeautifulSoup
import json
import sys

args = sys.argv

path = args[1]

filename = path.split("/")[-1].split(".")[0]

with open('data/'+filename+'.json') as f:
    arr = json.load(f)

"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/

export GOOGLE_APPLICATION_CREDENTIALS="/Users/nakamura/git/d_aozora/aozora_tei/src/text2speech/52478-e79637521a00.json"

"""
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# The response's audio_content is binary.
with open('data/'+filename+'.mp3', 'wb') as out:

    for i in range(len(arr)):

        print(str(i+1) + "/" + str(len(arr)))

        obj = arr[i]

        print(obj["text"])

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=obj["text"])

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL

        if obj["sex"] == 2: 
            ssml_gender = texttospeech.enums.SsmlVoiceGender.FEMALE
        elif obj["sex"] == 1:
            ssml_gender = texttospeech.enums.SsmlVoiceGender.MALE

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ja-JP',
            ssml_gender=ssml_gender)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        
        # Write the response to the output file.
        out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')