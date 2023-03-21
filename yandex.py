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


# todo: refactor class to upload not only to root
class YaUploader(YaInterface):
    """
    Uploader interface to manage post requests and upload data to cloud disk
    """

    def __init__(self, interface: YaInterface):
        super().__init__(interface.token)
        self.url = f'{self.url}/resources/upload'

    def get_upload_link(self, file_name: str) -> str:
        """
        Gets link needed to upload a file in cloud storage
        :param file_name: Desired name of a file in storage
        :return: String containing link for uploading a file
        """
        params = {'path': f'disk:/{file_name}'}
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.json()['href']

    # todo: refactor this method and make docstring
    def upload_file_to_root(self, file: str) -> None:
        if '/' not in file:
            href = self.get_upload_link(file)
        else:
            name = file[file.rfind('/') + 1:]
            href = self.get_upload_link(name)
        with open(file, 'rb') as f:
            response = requests.put(href, data=f)

        if response.status_code == 201:
            print(f'successfully uploaded {file} to root directory')
