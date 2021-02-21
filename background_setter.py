import random
import os
import ctypes

from constants import DOWNLOAD_PATH, SPI_SETDESKWALLPAPER


def get_random_file_link():
    files = os.listdir(DOWNLOAD_PATH)
    link = random.choice(files)
    return DOWNLOAD_PATH + link


def set_random_background():
    image_link = get_random_file_link()
    while not image_link.endswith(('.jpg', '.jpeg', '.png')):
        image_link = get_random_file_link()

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, get_random_file_link(), 0)
