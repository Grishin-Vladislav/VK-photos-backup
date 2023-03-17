import requests


# todo: refactor class to upload not only to root
class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_upload_link(self, file_name):
        headers = self.get_headers()
        params = {'path': f'disk:/{file_name}'}
        response = requests.get(f'{self.url}/resources/upload',
                                headers=headers, params=params)
        return response.json()

    def upload_file_to_root(self, file):
        if '/' not in file:
            href = self.get_upload_link(file)['href']
        else:
            name = file[file.rfind('/') + 1:]
            href = self.get_upload_link(name)['href']
        with open(file, 'rb') as f:
            response = requests.put(href, data=f)

        if response.status_code == 201:
            print(f'successfully uploaded {file} to root directory')
