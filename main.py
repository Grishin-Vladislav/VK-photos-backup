import os
from dotenv import load_dotenv, find_dotenv
from yandex import YaInterface, YaUploader

load_dotenv(find_dotenv())
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')

if __name__ == '__main__':
    ya = YaInterface(YANDEX_TOKEN)
    uploader = YaUploader(ya)
    uploader.upload_file_to_root('README.md')