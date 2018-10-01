import random

from OCR import *
from sentiment_analysis import *
from text_to_speech import *

def final_audio_from_image(img_file):#, audio_outpath):

    text = image_ocr(img_file)
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
    voice_audio = voiceOutput(pitch_offsets, genders, strs)#, audio_outpath)
    print(url_and_keyword)
    return url_and_keyword, voice_audio


if __name__ == '__main__':
    import sys
    #image_path = sys.argv[1]
    audio_outpath = 'output.mp3'
    # image_path = 'test-quotes.jpeg'
    with open(sys.argv[1], 'rb') as image_file:
        #print(final_audio_from_image(image_file, audio_outpath))
        urls, audio = final_audio_from_image(image_file)
    with open(audio_outpath, 'wb') as audio_file:
        audio_file.write(audio)
    print(urls)
