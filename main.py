import os
import requests  # delete
from dotenv import load_dotenv, find_dotenv
from yandex import YaInterface, YaUploader, YaDirectory
from pprint import pprint # delete

load_dotenv(find_dotenv())
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')

if __name__ == '__main__':
    ya = YaInterface(YANDEX_TOKEN)
    # uploader = YaUploader(ya)
    # uploader.upload_file('README.md', 'docs/test.md')
    directory = YaDirectory(ya)
    print(directory.check_path('docs/readme.md'))
    # directory.create_folder('docs')
    # uploader.upload_file_to_root('docs/README.md')