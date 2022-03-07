import os
import requests
from urllib import parse


def download_picture(url: str, filename: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as picture:
        picture.write(response.content)


def get_filename(comic_link: str) -> str:
    url_path = parse.urlsplit(comic_link).path
    filename = os.path.basename(url_path)
    return filename
