import random
import requests
from file_operations import get_filename


def get_number_of_all_episodes(base_url: str) -> int:
    url = f'{base_url}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    total_episodes = response.json()['num']
    return total_episodes


def get_comic_information(base_url: str, comic_episode: int) -> str:
    url = f'{base_url}{comic_episode}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_info = response.json()
    return comic_info


def get_comic_to_post() -> dict:
    base_url = 'https://xkcd.com/'
    total_episodes = get_number_of_all_episodes(base_url)
    random_episode = random.randint(0, total_episodes)
    comic_information = get_comic_information(base_url, random_episode)
    comic_to_post = {
        'comic_link': comic_information['img'],
        'comic_description': comic_information['alt'],
        'comic_filename': get_filename(comic_information['img'])
    }
    return comic_to_post
