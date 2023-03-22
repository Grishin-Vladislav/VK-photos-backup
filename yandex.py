import requests


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

    def __init__(self, interface: YaInterface):
        super().__init__(interface.token)
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
        return response.json()['href']

    def upload_file(self, link_to_file: str, destination: str) -> None:
        """
        Uploads file from url to cloud with desired file name.
        :param link_to_file: url to file to upload.
        :param destination: desired destination in cloud,
                ex:'docs/photos/meme.jpg'.
        """
        link = self.get_upload_link(destination)
        response = requests.get(link_to_file)
        requests.put(link, data=response.content)


class YaDirectory(YaInterface):
    """
    Directory manager for cloud storage
    """

    def __init__(self, interface: YaInterface):
        super().__init__(interface.token)
        self.url = f'{self.url}/resources'

    def check_path(self, path: str) -> bool:
        """
        Checks if directories or files exists
        :param path: directory path, ex:'docs/photos/meme.jpg'
        :return: True if all directories exists, else: False.
        """
        params = {'path': f'disk:/{path}'}
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            return True
        return False

    def create_folder(self, path: str) -> None:
        """
        Creates folder by given path, last destination will be desired folder
        :param path: path to desired folder ex:'docs/photos/memes'
        """
        params = {'path': f'disk:/{path}'}
        response = requests.put(self.url, headers=self.headers, params=params)
