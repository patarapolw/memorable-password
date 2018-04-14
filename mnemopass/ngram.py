import requests
from bs4 import BeautifulSoup
import string
from random import randrange


def generate_sentence(keyword):
    params = {
        'key': '* {} *'.format(keyword),
        'print_max': 100,
        'freq_threshold': 0,
        'output_style': 'sentence',
        'output_aux': 0,
        'print_format': 'text',
        'sort': None
    }

    r = requests.get('http://www.anc.org/cgi-bin/ngrams.cgi', params=params)

    text = BeautifulSoup(r.text, 'html.parser').text

    space = [-1]
    for i, char in enumerate(text):
        if char == ' ':
            try:
                if text[i+1] not in string.punctuation:
                    space.append(i)
            except ValueError:
                pass

    while True:
        try:
            start_index = randrange(len(space))
            start = space[start_index]
            end = space[start_index + 4]
            break
        except ValueError:
            pass

    return text[start:end]
