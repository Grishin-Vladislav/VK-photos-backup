import requests
import time


class YandexApi:
    def __init__(self, token: str):
        self.uploader = YaUploader(token)
        self.directory = YaDirectory(token)


class YaInterface:
    """
    Interface to provide base Yandex url,
     user token and auth request headers
    """
    url = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }


class YaUploader(YaInterface):
    """
    Interface to manage post requests and upload data to cloud disk
    """

    def __init__(self, token: str):
        super().__init__(token)
        self.url = f'{self.url}/resources/upload'

    def get_upload_link(self, file_path: str) -> str:
        """
        Gets link needed to upload a file in cloud storage
        :param file_path: Desired path to a file in cloud storage
                        ex:'docs/photos/meme.jpg'
        :return: String containing link for uploading a file
        """
        params = {'path': f'disk:/{file_path}'}
        response = requests.get(self.url, headers=self.headers, params=params)
        time.sleep(0.2)
        return response.json()['href']

    def upload_file_from_url(self, link_to_file: str, destination: str) -> None:
        """
        Uploads file from url to cloud with desired file name.
        :param link_to_file: url to file to upload.
        :param destination: desired destination in cloud,
                ex:'docs/photos/meme.jpg'.
        """
        link = self.get_upload_link(destination)
        response = requests.get(link_to_file)
        time.sleep(0.2)
        requests.put(link, data=response.content)
        time.sleep(0.2)

    def upload_from_data(self, data, destination: str) -> None:
        """
        uploads file straight from json object
        :param data: any python object
        :param destination: desired destination in cloud,
                ex:'docs/photos/meme.jpg'.
        """
        link = self.get_upload_link(destination)
        requests.put(link, data=data)
        time.sleep(0.2)


class YaDirectory(YaInterface):
    """
    Directory manager for cloud storage
    """

    def __init__(self, token: str):
        super().__init__(token)
        self.url = f'{self.url}/resources'

    def is_path_exists(self, path: str) -> bool:
        """
        Checks if directories or files exists
        :param path: directory path, ex:'docs/photos/meme.jpg'
        :return: True if all directories exists, else: False.
        """
        params = {'path': f'disk:/{path}'}
        response = requests.get(self.url, headers=self.headers, params=params)
        time.sleep(0.2)
        if response.status_code == 200:
            return True
        return False

    def create_folder(self, path: str) -> None:
        """
        Creates folder by given path, last destination will be desired folder
        :param path: path to desired folder ex:'docs/photos/memes'
        """
        params = {'path': f'disk:/{path}'}
        requests.put(self.url, headers=self.headers, params=params)
        time.sleep(0.2)
