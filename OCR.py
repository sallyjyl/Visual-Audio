import io
import os

# Google Cloud APIs
from google.cloud import vision

def image_ocr(file_path):
    # Get client
    client = vision.ImageAnnotatorClient()

    # Image raw bytes
    with io.open(file_path, 'rb') as file:
        content = file.read()

    image = vision.types.Image(content=content)

    # Perform OCR through cloud
    response = client.text_detection(image=image)

    # Hard code field values
    text = response.text_annotations[0].description

    return text


def get_quoted_strs(text):
    strs = text.split('\"')
    is_quoted = [(True if i % 2 == 1 else False) for i in range(len(strs))]
    return strs, is_quoted


if __name__ == '__main__':
    text = image_ocr('test-txt.jpeg')
    strs, is_quoted = get_quoted_strs(text)






