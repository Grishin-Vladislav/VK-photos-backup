import os
import requests  # delete
from dotenv import load_dotenv, find_dotenv
from yandex import YaInterface, YaUploader, YaDirectory
from vk import VkInterface, VkPhotos, VkUsers
from pprint import pprint  # delete

load_dotenv(find_dotenv())
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')

if __name__ == '__main__':
    pass
