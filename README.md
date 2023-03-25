# Vk photo backuper

Script for back-upping photos from Vk to Yandex Drive by vk user id.

## Installation (linux)

#### 1. Clone this repo or download zip archive and unpack it into desired folder.
#### 2. Check the requirements.txt file and install required python version.
#### 3. Open terminal in folder and create virtual environment:
```bash
python3 -m venv myenv
```
##### where "myenv" will be your desired virtual environment name
#### 4. Activate venv:
```bash
source myenv/bin/activate
```
#### 5. Create .env file and input your vk token and yandex disk token:
```text
YANDEX_TOKEN=heregoesyourtoken
VK_TOKEN=heregoesyourtoken
```

## Usage

```bash
python3 path/to/file/main.py
```