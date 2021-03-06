import io
import os
import re

# Google Cloud APIs
from google.cloud import vision

def image_ocr(file, filename=None):
    # Get client
    client = vision.ImageAnnotatorClient()

    # Image raw bytes
    content = file.read()
    image = vision.types.Image(content=content)
    # Perform OCR through cloud
    response = client.text_detection(image=image)

    if response.text_annotations:
        # Hard code field values
        text = response.text_annotations[0].description
    else:
        print('Input file {}not supported'.format(filename + ' ' if filename else ''))
        text = ''

    return text


def split_str_and_get_quoted(text):
    chars = list(text)

    # Convert '\n' to periods or spaces
    for i, c in enumerate(chars):
        if c == '\n':
            if i < len(chars) - 1 and chars[i + 1].isupper():
                chars[i] = '. '
            else:
                chars[i] = ' '

    text = ''.join(chars)

    # Split by quotes, filter, to get quoted strings
    strs = text.split('\"')
    good_strs = []
    for s in strs:
        if re.search('[A-Za-z]', s):
            good_strs.append(s)

    quoted_indices = list(range(1, len(strs), 2))
    return strs, quoted_indices


if __name__ == '__main__':
    with io.open("test-txt.jpeg", "rb") as file:
        text = image_ocr(file)
    strs, quoted_indices = split_str_and_get_quoted(text)






