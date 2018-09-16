import six
import sys
import random
import argparse
import requests

from google.cloud import language
from google.cloud import language_v1
from google.cloud.language import types
from google.cloud.language_v1 import enums

def analyze_sentiment(content):

    client = language_v1.LanguageServiceClient()

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment

    return sentiment.score


def classify_text(text):
    """Classifies content categories of the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    categories = client.classify_text(document).categories

    for category in categories:
        print(u'=' * 20)
        print(u'{:<16}: {}'.format('name', category.name))
        print(u'{:<16}: {}'.format('confidence', category.confidence))
        return category.name.split(' ')[-1] #only the last, most specific noun as the image to be displayed


def search_for_image(input_keyword):
    search_query = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCVPDYrTm2h_keElXO1iAW-PW5RAlujEtg&cx=017480567514037437480%3Akvmd1lv2ahm&q=" + str(input_keyword) + "&searchType=image&fileType=jpg&imgSize=medium&num=10"
    # r = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyCVPDYrTm2h_keElXO1iAW-PW5RAlujEtg&cx=017480567514037437480%3Akvmd1lv2ahm&q=flower&searchType=image&fileType=jpg&imgSize=medium&num=1")
    r = requests.get(search_query)

    intermediate = r.json()
    # Get a random image url
    if 'items' not in intermediate:
        return search_for_image('socks')
    else:
        return random.choice(intermediate['items'])['link']

def download_jpg(pic_url):
    with open('pic_1.jpg', 'wb+') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

