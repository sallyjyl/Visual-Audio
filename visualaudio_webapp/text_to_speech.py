"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from google.cloud import translate

##Hardcoded list for supported list"
VOICE={
  "en-US": {
     "f" : {
        "Standard": ["C", "E"],
        "Wavenet": ["C", "E", "F"]
     },
     "m" : {
        "Standard": ["B", "D"],
        "Wavenet": ["A", "B", "D"]
     }
  }
}

def clip_value(val, lo, hi):
    return min(hi, max(val, lo))

def voiceOutput(pitchInput, genderInput, textInput):#, filename):
    #with open(filename, 'wb') as out:
        # Set the text input to be synthesized
        audio_data = b''
        for i in range (len(textInput)):
            # Instantiates a client
            client = texttospeech.TextToSpeechClient()
            lang = detectLanguage(textInput[i])

            # Hardcode to skip non enlglish
            if lang != 'en':
                continue
            lang = matchCountryCode(lang)

            synthesis_input = texttospeech.types.SynthesisInput(text=textInput[i])

            if (genderInput[i] == 'f'):
                gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            else:
                gender = texttospeech.enums.SsmlVoiceGender.MALE

            name_input=returnVoiceName(lang, genderInput[i], "Wavenet")

            print (name_input);
            # Build the voice request, select the language code ("en-US") and the ssml
            # voice gender ("neutral")
            voice = texttospeech.types.VoiceSelectionParams(
                language_code=lang,
                name=name_input,
                ssml_gender=gender)

            pace = 0.8
            if abs(pitchInput[i]) >= 6:
                pace += 0.2

            # Select the type of audio file you want returned
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                pitch=clip_value(pitchInput[i] - 3, -20, 20),
                speaking_rate=pace) # 1 is the normal speed

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(synthesis_input, voice, audio_config)

            #responseArray.extend(response)

            #out.write(response.audio_content)
            audio_data += response.audio_content
        return audio_data
        # The response's audio_content is binary.
            # Write the response to the output file.
            #for response in responseArray:

    #print("Audio content written to file " + filename)

def detectLanguage(text):
    translate_client = translate.Client()
    result = translate_client.detect_language(text)
    res = format(result['language'])
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

def returnVoiceName(lang, gender, voiceType):
    ##Currently by default return the first one available.
    return lang + "-" + voiceType + "-" + VOICE[lang][gender][voiceType][0]