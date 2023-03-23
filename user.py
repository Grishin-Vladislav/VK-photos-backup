from yandex import YandexApi
from vk import VkApi


class User:
    def __init__(self, vk_token, ya_token):
        self.yandex = YandexApi(ya_token)
        self.vk = VkApi(vk_token)
