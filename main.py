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


def get_profile_album(user_id: str, photo_interface: VkPhotos) -> dict:
    """
    Get short info about user's profile album.
    :param user_id: desired vk profile id.
    :param photo_interface: instance of VkPhotos class.
    :return: dictionary with info about album.
    """
    raw_data = photo_interface.get_profile_photos(user_id)
    info = {'count': int(raw_data['response']['count']), 'items': []}
    for item in raw_data['response']['items']:
        album_photo = {
            'date': datetime.fromtimestamp(item['date']).strftime('%d.%m.%Y_%H.%M'),
            'likes': int(item['likes']['count']),
            'photo': {
                'type': item['sizes'][-1]['type'],
                'url': item['sizes'][-1]['url']
            }
        }
        info['items'].append(album_photo)
    return info


if __name__ == '__main__':
    vk = VkInterface(VK_TOKEN)
    ya = YaInterface(YANDEX_TOKEN)

    user_id = input('Введите id пользователя Вконтакте: \n')
    user_interface = VkUsers(vk)

    # pprint(user.get_user_info(user_id))  # test
    if is_valid_user_id(user_id, user_interface):
        photo_manager = VkPhotos(vk)
        profile_photos = get_profile_album(user_id, photo_manager)
        amount = input(f'В альбоме {profile_photos["count"]} фото, '
                       f'сколько последних фото сохранить?\n')
