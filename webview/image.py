import requests


def load_image(search_term):
    headers = {
        "Ocp-Apim-Subscription-Key": '552d465f202e4f839d0d4df65bafb3f5'
    }
    params = {
        "q": search_term,
        "textDecorations": True,
        "textFormat": "HTML"
    }
    response = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/images/search',
                            headers=headers, params=params)
    response.raise_for_status()

    return response.json()['value'][0]['contentUrl']


if __name__ == '__main__':
    print(load_image('hello'))