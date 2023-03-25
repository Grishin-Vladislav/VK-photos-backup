import os
from dotenv import load_dotenv, find_dotenv
from backuper import YaDiskBackuper


load_dotenv(find_dotenv())
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')


if __name__ == '__main__':
    backup = YaDiskBackuper(VK_TOKEN, YANDEX_TOKEN)

    user_id = input('Введите id пользователя Вконтакте: \n')

    backup.backup(user_id)
