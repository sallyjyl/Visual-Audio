"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from google.cloud import translate

def voiceOutput(pitchInput, genderInput, textInput, filename):
    #responseArray = []

    with open(filename, 'wb') as out:
        # Set the text input to be synthesized
        for i in range (len(textInput)):

            print(textInput[i])

            # Instantiates a client
            client = texttospeech.TextToSpeechClient()
            lang = detectLanguage(textInput[i])
            synthesis_input = texttospeech.types.SynthesisInput(text=textInput[i])
            if (genderInput[i] == 'f'):
                gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            else:
                gender = texttospeech.enums.SsmlVoiceGender.MALE

            # Build the voice request, select the language code ("en-US") and the ssml
            # voice gender ("neutral")
            voice = texttospeech.types.VoiceSelectionParams(
                language_code=lang,
                ssml_gender=gender)

            # Select the type of audio file you want returned
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                pitch=pitchInput[i],
                speaking_rate=0.8) # 1 is the normal speed

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(synthesis_input, voice, audio_config)

            #responseArray.extend(response)

            out.write(response.audio_content)
        # The response's audio_content is binary.
            # Write the response to the output file.
            #for response in responseArray:

    print("Audio content written to file " + filename)

def detectLanguage(text):
    translate_client = translate.Client()
    result = translate_client.detect_language(text)
    res = format(result['language'])
    # Filter unknown
    if res == 'und':
        res = 'en'
    return res

def matchCountryCode(lang):
    if lang in ["nl", "en", "fr", "de", "it", "ja", "ko", "es", "pt", "sv", "tr"]:
        ##Some default accents
        if (lang == "en"):
            return "en-US"
        elif (lang == "ja"):
            return "ja-JP"
        elif (lang == "ko"):
            return "ko-KR"
        elif (lang=="sv"):
            return "sv-SE"
        else:
            return lang+"-"+lang.upper()
    else: ##Not supported by google
        return "en-US"
