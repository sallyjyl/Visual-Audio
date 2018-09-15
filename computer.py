from OCR import *
from sentiment_analysis import *
from audio_synthesis import *


def final_audio_from_image(img_path):

    text = image_ocr(img_path)
    strs, quoted_indices = split_str_and_get_quoted(text)
    # sentiments = [analyze_sentiment(strs[i]) for i in quoted_indices]

    # Calculate sentiment for each string
    # 0 if not quoted
    sentiments = []
    for i in range(len(strs)):
        if i not in quoted_indices:
            sentiments.append(0)
        else:
            sentiment = sample_analyze_sentiment(strs[i])
            sentiments.append(sentiment)

    ''' testing '''
    print('strs:\n', strs)
    print('sentiments:\n', sentiments)

    # Calculate pitch offset for each string
    pitch_amp_constant = 20
    pitch_offsets = [sent * pitch_amp_constant for sent in sentiments]

    final_audio = generate_audio(strs, pitch_offsets)
    return final_audio



if __name__ == '__main__':

    image_path = 'test-txt.jpeg'


    pass