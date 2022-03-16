import os
import requests
from dotenv import load_dotenv
from vk_api import publish_comic
from xkcd import get_comic_to_post
from file_operations import download_picture


def main():
    load_dotenv()
    try:
        comic = get_comic_to_post()
        download_picture(comic['comic_link'], comic['comic_filename'])
        publish_comic(comic)
    except requests.exceptions.HTTPError as http_error:
        print(f'Что-то пошло не так..\n{http_error.response}')
    except IOError:
        print('Не получилось скачать файл')
    finally:
        os.remove(comic['comic_filename'])


if __name__=='__main__':
    main()
