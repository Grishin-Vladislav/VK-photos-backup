from yandex import YandexApi
from vk import VkApi
from datetime import datetime
import json


class YaDiskBackuper:
    def __init__(self, vk_token, ya_token):
        self.__yandex = YandexApi(ya_token)
        self.__vk = VkApi(vk_token)

    def backup(self, user_id) -> None:
        """
        Backups photos from __vk page album to __yandex cloud drive by user id
        :param user_id: Vk user id
        """
        if not self.is_valid_user_id(user_id):
            return

        user_name = self.__vk.users.get_user_full_name(user_id)
        photo_album = self.__vk.photos.get_profile_photos(user_id)
        amount = int(input(f'В альбоме {photo_album["response"]["count"]}'
                           f' фото, сколько последних фото сохранить?\n'))
        meta = self.get_meta_from_photo_album(user_name, photo_album, amount)
        self.make_directories_in_cloud(meta)
        self.upload_photos_to_yadisk(meta)
        result = self.upload_json_to_yadisk(meta)
        print(result)

    def is_valid_user_id(self, user_id: str) -> bool:
        """
        Check if entered id is correct and profile is open.
        :param user_id: desired __vk profile id.
        :return: True if user has desired info else False.
        """
        profile_info = self.__vk.users.get_user_info(user_id)
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

    @staticmethod
    def get_meta_from_photo_album(name: str, album: dict, amount: int) -> dict:
        """
        Forms metadata needed to upload files to Yandex cloud.
        :param name: user's credentials ex. 'Павел Дуров'.
        :param album: dictionary from vkapi/photos.get request.
        :param amount: desired amount of photos to upload.
        :return: dictionary with metadata which also includes filename.
        """
        meta = {'name': name, 'items': []}
        for item in album['response']['items'][:amount]:
            date = datetime.fromtimestamp(item['date']).strftime(
                '%d.%m.%Y_%H.%M')
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

            meta['items'].append({
                'date': date,
                'likes': likes,
                'photo': {
                    'type': res_type[0],
                    'url': url
                }
            })

        likes = [i['likes'] for i in meta['items']]

        for photo in meta['items']:
            photo_likes = photo['likes']
            date = photo['date']
            if photo_likes in likes and likes.count(photo_likes) > 1:
                photo['filename'] = f'{photo_likes}_{date}.jpg'
            else:
                photo['filename'] = f'{photo_likes}.jpg'

        return meta

    def make_directories_in_cloud(self, meta: dict) -> None:
        """
        Prepares directories on Yandex cloud drive for album.
        :param meta: metadata of photo album.
        """
        root = 'vk_photos_backup'
        user_folder = meta['name']
        if not self.__yandex.directory.check_path(root):
            self.__yandex.directory.create_folder(root)
            self.__yandex.directory.create_folder(f'{root}/{user_folder}')
        elif not self.__yandex.directory.check_path(f'{root}/{user_folder}'):
            self.__yandex.directory.create_folder(f'{root}/{user_folder}')
        else:
            pass

    def upload_photos_to_yadisk(self, meta: dict) -> None:
        """
        Extracts needed data from meta and upload files to yadisk.
        :param meta: metadata of photo album.
        """
        base_path = f'vk_photos_backup/{meta["name"]}'
        for photo in meta['items']:
            full_path = f'{base_path}/{photo["filename"]}'
            link = photo['photo']['url']
            self.__yandex.uploader.upload_file_from_url(link, full_path)

    def upload_json_to_yadisk(self, meta: dict) -> json:
        """
        refactors meta and uploads it to yadisk
        :param meta: metadata of photo album.
        :return json: returns clean metadata including filename and size type
        """
        clean_meta = []
        for photo in meta['items']:
            data = {
                'filename': photo['filename'],
                'size': photo['photo']['type']
            }
            clean_meta.append(data)
        clean_meta = json.dumps(clean_meta, indent=4, ensure_ascii=False)
        path = f'vk_photos_backup/{meta["name"]}/meta.json'
        self.__yandex.uploader.upload_from_data(clean_meta, path)
        return clean_meta
