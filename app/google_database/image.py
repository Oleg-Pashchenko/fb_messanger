import shutil
import requests
from pyjpgclipboard import clipboard_dump_jpg, clipboard_load_jpg


def download_image(link: str):
    link = link.split('d/')[1].split('/')[0]
    link = f'https://drive.usercontent.google.com/u/0/uc?id={link}&export=download'
    response = requests.get(link, stream=True)
    with open('1.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    clipboard_load_jpg("1.jpg")


