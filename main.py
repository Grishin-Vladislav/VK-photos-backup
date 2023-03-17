import os
from dotenv import load_dotenv, find_dotenv
from yandex import YaUploader

load_dotenv(find_dotenv())
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')

if __name__ == '__main__':
    print('hello world')
