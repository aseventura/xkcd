import random
import requests
from file_operations import get_filename


def get_number_of_all_episodes() -> int:
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    total_episodes = response.json()['num']
    return total_episodes


def get_comic_information(comic_episode: int) -> str:
    url = f'https://xkcd.com/{comic_episode}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_info = response.json()
    return comic_info


def get_comic_to_post() -> dict:
    total_episodes = get_number_of_all_episodes()
    random_episode = random.randint(0, total_episodes)
    comic_information = get_comic_information(random_episode)
    comic_to_post = {
        'comic_link': comic_information['img'],
        'comic_description': comic_information['alt'],
        'comic_filename': get_filename(comic_information['img'])
    }
    return comic_to_post
