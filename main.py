import os
import requests  # delete
from dotenv import load_dotenv, find_dotenv
from yandex import YaInterface, YaUploader, YaDirectory
from vk import VkInterface, VkPhotos, VkUsers
from pprint import pprint  # delete
from datetime import datetime

load_dotenv(find_dotenv())
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')


def is_valid_user_id(user_id: str, user_interface: VkUsers) -> bool:
    """
    Check if entered id is correct and profile is open.
    :param user_id: desired vk profile id.
    :param user_interface: instance of VkUsers class.
    :return: True if user has desired info else False.
    """
    profile_info = user_interface.get_user_info(user_id)
    if not profile_info['response']:
        print('Неверный id пользователя')

    elif profile_info['response'][0]['is_closed'] \
            and not profile_info['response'][0]['can_access_closed']:
        print('Пользователь скрыл профиль')

    elif profile_info['response'][0].get('deactivated'):
        print('Профиль пользователя удалён')

    else:
        print('Профиль пользователя подходит')
        return True

    return False


def get_meta_from_photo_album(album: dict, amount: dict) -> dict:
    # todo: split this func
    """
    Forms metadata needed to upload files to cloud.
    :param album: dictionary from vkapi/photos.get request.
    :param amount: desired amount of photos to upload.
    :return: dictionary with metadata which also includes filename.
    """
    meta = {}
    for indx, item in enumerate(album['response']['items'][:amount], 1):
        date = datetime.fromtimestamp(item['date']).strftime('%d.%m.%Y_%H.%M')
        likes = int(item['likes']['count'])

        has_max_resolution = False
        max_res_index = 0
        for i, size in enumerate(item['sizes']):
            if size['type'] == 'w':
                has_max_resolution = True
                max_res_index = i
                break

        if has_max_resolution:
            res_type = 'w'
            url = item['sizes'][max_res_index]['url']
        else:
            res_type = item['sizes'][-1]['type'],
            url = item['sizes'][-1]['url']

        meta[f'photo{indx}'] = {
            'date': date,
            'likes': likes,
            'photo': {
                'type': res_type,
                'url': url
            }
        }

    likes = [i['likes'] for i in meta.values()]

    for photo in meta.keys():
        photo_likes = meta[photo]['likes']
        date = meta[photo]['date']
        if photo_likes in likes and likes.count(photo_likes) > 1:
            meta[photo]['filename'] = f'{photo_likes}_{date}.jpg'
        else:
            meta[photo]['filename'] = f'{photo_likes}.jpg'

    return meta


def make_directories_in_cloud(photo_data: dict, dir_manager: YaDirectory) -> None:
    # todo: make this func to create folder with the name of user, refactor get_meta() for this to include credentials
    """
    Prepares directories on Yandex cloud drive for album.
    :param photo_data: metadata of photo album.
    :param dir_manager: instance of YaDirectory, to manage folders with.
    """
    pass


if __name__ == '__main__':
    vk = VkInterface(VK_TOKEN)
    ya = YaInterface(YANDEX_TOKEN)

    user_id = input('Введите id пользователя Вконтакте: \n')  # 3383304
    user_interface = VkUsers(vk)

    if is_valid_user_id(user_id, user_interface):
        photo_manager = VkPhotos(vk)
        profile_photos = photo_manager.get_profile_photos(user_id)
        amount = int(input(f'В альбоме {profile_photos["response"]["count"]}'
                           f' фото, сколько последних фото сохранить?\n'))
        meta = get_meta_from_photo_album(profile_photos, amount)

        directory_manager = YaDirectory(ya)
        make_directories_in_cloud(meta, directory_manager)