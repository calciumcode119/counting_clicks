import requests
import os
from dotenv import load_dotenv
from prettyprinter import pprint
from urllib.parse import urlparse


def shorten_link(token, url):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Cookie': 'beget=begetok',
    }
    data = {
        'url': url,
    }
    response = requests.post(
        'https://clc.li/api/url/add',
        headers=headers,
        json=data,
        )
    response.raise_for_status()
    parsed_url = urlparse(response.json()['shorturl'])
    shorten_url = parsed_url.netloc + parsed_url.path
    return shorten_url


def count_clicks(token, url):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Cookie': 'beget=begetok',
    }
    response = requests.get(
        'https://clc.li/api/urls?short={}'.format(url),
        headers=headers,
        )
    response.raise_for_status()
    return response.json()['data']['clicks']


def is_bitlink(token, url):
    is_bitlink = False
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Cookie': 'beget=begetok',
    }
    response = requests.get(
        'https://clc.li/api/urls?short={}'.format(url),
        headers=headers,
        )
    response.raise_for_status()
    is_bitlink = not response.json()['error']
    return is_bitlink


def main():
    load_dotenv()
    api_key = os.environ['API_KEY']
    user_input = input('Введите ссылку: ')
    if is_bitlink(api_key, user_input):
        try:
            print('Количество кликов:', end=' ')
            print(count_clicks(api_key, user_input))
        except KeyError:
            print('Ссылка некорректна. Проверьте точность написания.')
    else:
        try:
            print('Короткая ссылка:', shorten_link(api_key, user_input))
        except KeyError:
            print('Ссылка некорректна. Проверьте точность написания.') 


if __name__ == '__main__':
    main()
