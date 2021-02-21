import os
import re
from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup

from constants import *


def get_local_html(url):
    r = requests.get(url)
    with open(LOCAL_URL, 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)


def get_images_links(theme, resolution, page=1):
    if theme != 'all':
        theme = 'catalog/' + theme
    if page == 1:
        page = ''
    else:
        page = 'page' + str(page)
    url = MAIN_URL + theme + '/' + resolution + '/' + page
    print(url)
    get_local_html(url)
    with open(LOCAL_URL) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    images_links = []
    for raw_data in soup.find_all('a', {'class': IMG_LINK_CLASS}):
        link = raw_data.get('href')
        link = re.sub('/' + resolution, '_' + resolution + '.jpg', link)
        link = re.sub('/download', 'image', link)
        link = DOWNLOAD_URL + link
        images_links.append(link)
    return images_links


def download_image(theme=DEFAULT_THEME, resolution=DEFAULT_RESOLUTION, page=1):
    links = get_images_links(theme, resolution, page)
    for link in links:
        name = get_name_by_link(link)
        if is_file_exists(DOWNLOAD_PATH + name):
            continue
        print(name)
        response = requests.get(link)
        image = Image.open(BytesIO(response.content))
        image.save(DOWNLOAD_PATH + name)
        return
    download_image(page=page+1)


def get_name_by_link(link):
    return re.split('/', link)[-1]


def is_file_exists(path):
    return os.path.isfile(path)


'''
def get_src_and_alt(res, theme):
    if theme == '':
        theme = 'all'
    else:
        theme = 'catalog/' + theme
    url = MAIN_URL + theme + '/' + res
    print(url)
    get_local_html(url)

    with open(LOCAL_URL) as fp:
        soup = BeautifulSoup(fp, 'lxml')

    # Находим все вхождения div с классом wallpaper_pre
    imgs = soup.find_all('div', {'class': 'wallpaper_pre'})

    srcs = []
    # Записываем "сырые" данные о ссылке и описании в srcs
    for img in imgs:
        wall = {}
        wall['src'] = img.find('a').get('href')
        wall['alt'] = img.find('img').get('alt')
        srcs.append(wall)

    # "Чистим" описание от запятых и получаем чистую ссылку на обои
    for src in srcs:
        src['alt'] = re.sub(',', '', src['alt'])
        src['alt'] = re.sub('Preview wallpaper', '', src['alt'])
        src['alt'] = src['alt'].split()

        src['src'] = re.sub('download', 'image', src['src'])
        src['src'] = re.sub('/' + res, '_' + res + '.jpg', src['src'])

    return srcs
'''
