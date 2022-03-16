import os
import requests


def check_vkresponse_on_error(response):
    vk_response = response.json()
    if 'error' in vk_response:
        raise requests.exceptions.HTTPError(response=vk_response['error']['error_msg'])
    return vk_response


def get_url_for_picture_upload(access_token: str, group_id: str):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'v': '5.131',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    vk_response = check_vkresponse_on_error(response)
    upload_url = vk_response['response']['upload_url']
    return upload_url


def upload_comic_on_server(upload_url: str, comic_filename: str):
    with open(comic_filename, 'rb') as picture:
        files = {
            'file1': picture,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        server_response = response.json()
    return server_response


def save_photo_on_vk_server(access_token: str, group_id: str, upload_url: str, comic: dict):
    server_response = upload_comic_on_server(upload_url, comic['comic_filename'])
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    header = {
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        'group_id': group_id,
        'photo': server_response['photo'],
        'server': server_response['server'],
        'hash': server_response['hash'],
        'caption': comic['comic_description'],
        'v': '5.131',
    }
    response = requests.post(url=url, headers=header, data=data)
    response.raise_for_status()
    vk_response = check_vkresponse_on_error(response)
    picture_information = vk_response['response'][0]
    return picture_information


def publish_post_in_vk(access_token: str, group_id: str, upload_url: str, comic: dict):
    picture_information = save_photo_on_vk_server(access_token, group_id, upload_url, comic)
    url = 'https://api.vk.com/method/wall.post'
    header = {
        'Authorization': f'Bearer {access_token}',
    }
    owner_id = f'-{group_id}'
    data = {
        'owner_id': owner_id,
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(picture_information['owner_id'], picture_information['id']),
        'message': picture_information['text'],
        'v': '5.131',
    }
    response = requests.post(url, headers=header, data=data)
    response.raise_for_status()
    check_vkresponse_on_error(response)


def publish_comic(comic: dict):
    group_id = os.getenv('PUBLIC_ID')
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    upload_url = get_url_for_picture_upload(vk_access_token, group_id)
    publish_post_in_vk(vk_access_token, group_id, upload_url, comic)
