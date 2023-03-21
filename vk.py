import requests


class VkInterface:
    """
    An interface to provide base VK url,
     user token and auth request params
    """
    url = 'https://api.vk.com/method'

    def __init__(self, token: str):
        self.token = token
        self.params = {
            'access_token': token,
            'v': '5.131',
        }

