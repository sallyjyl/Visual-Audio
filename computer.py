import random

from OCR import *
from sentiment_analysis import *
from text_to_speech import *

def final_audio_from_image(img_path, audio_outpath):

    text = image_ocr(img_path)
    strs, quoted_indices = split_str_and_get_quoted(text)

    # Calculate sentiment for each string
    # 0 if not quoted
    sentiments = []
    url_and_keyword = []
    for i in range(len(strs)):
        if i not in quoted_indices:
            sentiments.append(0)
        else:
            sentiment = analyze_sentiment(strs[i])
            sentiments.append(sentiment)

        words = [word for word in re.split(' +', strs[i]) if word != '']
        strs[i] = ' '.join(words)
        new_s = ''
        if words:
            for j in range(40 // len(words)):
                new_s += ' ' + strs[i]
            summary_word = str(classify_text(new_s)).replace('/', '')
            url_and_keyword.append((search_for_image(summary_word), summary_word))

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

    # Make audio
    voiceOutput(pitch_offsets, genders, strs, audio_outpath)
    return url_and_keyword


if __name__ == '__main__':
    import sys
    image_path = sys.argv[1]
    audio_outpath = 'output.mp3'
    # image_path = 'test-quotes.jpeg'
    print(final_audio_from_image(image_path, audio_outpath))

