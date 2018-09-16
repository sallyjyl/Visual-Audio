import random

from OCR import *
from sentiment_analysis import *
from text_to_speech import *

def final_audio_from_image(img_path):

    text = image_ocr(img_path)
    strs, quoted_indices = split_str_and_get_quoted(text)

    # Calculate sentiment for each string
    # 0 if not quoted
    sentiments = []
    for i in range(len(strs)):
        if i not in quoted_indices:
            sentiments.append(0)
        else:
            sentiment = analyze_sentiment(strs[i])
            sentiments.append(sentiment)

    ''' testing '''
    print('strs:\n', strs)
    print('sentiments:\n', sentiments)


    # Calculate pitch offset for each string
    pitch_amp_constant = 30
    pitch_offsets = [sent * pitch_amp_constant for sent in sentiments]

    # Fake genders for reading for now
    default_gender = 'f'
    genders = []
    for i in range(len(strs)):
        if i in quoted_indices:
            genders.append('m')
        else:
            genders.append(default_gender)

    audio_filename = 'audio_shaw.mp3'

    # Make audio
    voiceOutput(pitch_offsets, genders, strs, audio_filename)


if __name__ == '__main__':
    import sys
    image_path = sys.argv[1]
    # image_path = 'test-quotes.jpeg'
    final_audio_from_image(image_path)

