import time
import requests


class VkApi:
    def __init__(self, token: str):
        self.photos = VkPhotos(token)
        self.users = VkUsers(token)


class VkInterface:
    """
    Interface to provide base VK url,
     user token and auth request params
    """
    url = 'https://api.vk.com/method'

    def __init__(self, token: str):
        self.token = token
        self.params = {
            'access_token': token,
            'v': '5.131',
        }


class VkPhotos(VkInterface):
    """
    Interface to get photo's info from user albums
    """

    def __init__(self, token: str):
        super().__init__(token)
        self.url = f'{self.url}/photos.get'

    def get_profile_photos(self, user_id: str) -> dict:
        """
        Gets full info about profile photo album
        :param user_id: desired user id.
        :return: dictionary with album info.
        """
        params = {
            **self.params,
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'rev': 1
        }
        response = requests.get(self.url, params=params)
        time.sleep(0.33)
        return response.json()


class VkUsers(VkInterface):
    """
    Interface to manage user data
    """

    def __init__(self, token: str):
        super().__init__(token)
        self.url = f'{self.url}/users.get'

    def get_user_full_name(self, user_id: str) -> str:
        """
        gets profile page credentials from user id
        :param user_id: desired user id
        :return: string ex. 'Павел Дуров'
        """
        profile_info = self.get_user_info(user_id)
        name = profile_info['response'][0]['first_name']
        surname = profile_info['response'][0]['last_name']
        return f'{name} {surname}'

    def get_user_info(self, user_id: str) -> dict:
        """
        gets user info by user id.
        :param user_id: desired user id.
        :return: dictionary with user info.
        """
        params = {
            **self.params,
            'fields': 'crop_photo, has_photo, photo_max_orig',
            'user_ids': user_id
        }
        response = requests.get(self.url, params=params)
        time.sleep(0.33)
        return response.json()
