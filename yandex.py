import requests


class YaInterface:
    """
    An interface to provide base Yandex url,
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
    Uploader interface to manage post requests and upload data to cloud disk
    """

    def __init__(self, interface: YaInterface):
        super().__init__(interface.token)
        self.url = f'{self.url}/resources/upload'

    def get_upload_link(self, file_path: str) -> str:
        """
        Gets link needed to upload a file in cloud storage
        :param file_path: Desired path to a file in cloud storage
        :return: String containing link for uploading a file
        """
        params = {'path': f'disk:/{file_path}'}
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.json()['href']

    def upload_file(self, local_file_path: str, destination: str) -> None:
        """
        Uploads file from disk to cloud with desired file name.
        :param local_file_path: path to file to upload.
        :param destination: desired destination in cloud,
                must include tail -> desired file name.
        """
        link = self.get_upload_link(destination)
        with open(local_file_path, 'rb') as f:
            requests.put(link, data=f)


class YaDirectory(YaInterface):
    """
    Directory manager for cloud storage
    """

    def __init__(self, interface: YaInterface):
        super().__init__(interface.token)
        self.url = f'{self.url}/resources'

    def create_folder(self, path: str) -> None:
        """
        Creates folder by given path, last destination will be desired filename
        :param path: path to desired folder ex:'docs/photos/memes'
        """
        params = {'path': f'disk:/{path}'}
        response = requests.put(self.url, headers=self.headers, params=params)
