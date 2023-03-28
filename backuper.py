from yandex import YandexApi
from vk import VkApi
from datetime import datetime
import json
from tqdm import tqdm


class YaDiskBackuper:
    def __init__(self, vk_token, ya_token):
        self.__yandex = YandexApi(ya_token)
        self.__vk = VkApi(vk_token)

    def backup(self) -> None:
        """
        Backups photos from vk page album to yandex cloud drive by user id
        """
        while True:
            user_id = input('Введите id пользователя Вконтакте: \n')
            print('Проверка информации о пользователе...', flush=True)
            if self.__is_valid_user_id(user_id):
                break
        user_name = self.__vk.users.get_user_full_name(user_id)

        print('Получение альбома пользователя...', flush=True)
        photo_album = self.__vk.photos.get_profile_photos(user_id)
        print('ОК', flush=True)

        while True:
            total = photo_album["response"]["count"]
            amount = input(f'В альбоме {total} фото, сколько последних'
                           f' фото сохранить?\n')
            if self.__is_valid_amount(amount, total):
                amount = int(amount)
                break
            print('Некорректный ввод')

        print('Подготовка метаданных для загрузки...', flush=True)
        meta = self.__get_meta_from_photo_album(photo_album, amount)
        print('ОК', flush=True)

        print('Подготовка директорий в облаке...', flush=True)
        self.__make_directories_in_cloud(user_name)
        print('ОК', flush=True)

        print('Загрузка фото в облачное хранилище...', flush=True)
        self.__upload_photos_to_yadisk(meta, user_name)
        print('ОК', flush=True)

        print('Сохранение данных о загруженных фотографиях...', flush=True)
        result = self.__upload_json_to_yadisk(meta, user_name)
        print('ОК', flush=True)
        print(result)

    def __is_valid_user_id(self, user_id: str) -> bool:
        """
        Check if entered id is correct and profile is open.
        :param user_id: desired vk profile id.
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
    def __is_valid_amount(amount: str, total: int) -> bool:
        """
        Checks if entered valid number of photos.
        :param amount: desired amount of photos.
        :param total: max photos in album.
        :return: True if instance is valid else False.
        """
        if amount.isdigit() and 0 <= int(amount) <= total:
            return True
        return False

    @staticmethod
    def __get_meta_from_photo_album(album: dict, amount: int) -> dict:
        """
        Forms metadata needed to upload files to Yandex cloud.
        :param album: dictionary from vkapi/photos.get request.
        :param amount: desired amount of photos to upload.
        :return: dictionary with metadata which also includes filename.
        """
        meta = {'items': []}
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

    def __make_directories_in_cloud(self, folder_name: str) -> None:
        """
        Prepares directories on Yandex cloud drive for album.
        :param folder_name: name of the destination folder.
        """
        root = 'vk_photos_backup'
        if not self.__yandex.directory.is_path_exists(root):
            self.__yandex.directory.create_folder(root)
            self.__yandex.directory.create_folder(f'{root}/{folder_name}')
        elif not self.__yandex.directory.is_path_exists(
                f'{root}/{folder_name}'):
            self.__yandex.directory.create_folder(f'{root}/{folder_name}')
        else:
            pass

    def __upload_photos_to_yadisk(self, meta: dict, folder_name: str) -> None:
        """
        Extracts needed data from meta and upload files to yadisk.
        :param meta: metadata of photo album.
        :param folder_name: name of the destination.
        """
        base_path = f'vk_photos_backup/{folder_name}'
        for photo in tqdm(meta['items'], desc='progress'):
            full_path = f'{base_path}/{photo["filename"]}'
            link = photo['photo']['url']
            self.__yandex.uploader.upload_file_from_url(link, full_path)

    def __upload_json_to_yadisk(self, meta: dict, folder_name: str) -> json:
        """
        refactors meta and uploads it to yadisk
        :param meta: metadata of photo album.
        :param folder_name: name of destination folder.
        :return json: returns clean metadata including filename and size type.
        """
        clean_meta = []
        for photo in meta['items']:
            data = {
                'filename': photo['filename'],
                'size': photo['photo']['type']
            }
            clean_meta.append(data)
        clean_meta = json.dumps(clean_meta, indent=4, ensure_ascii=False)
        path = f'vk_photos_backup/{folder_name}/meta.json'
        self.__yandex.uploader.upload_from_data(clean_meta, path)
        return clean_meta
