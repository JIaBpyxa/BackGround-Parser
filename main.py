from bs4 import BeautifulSoup
import requests
import re


def get_local(url):
    '''
    :param url: Адрес сайта
    :param res: Разрешение нужных обоев
    :return: Создает локальный файл-копию сайта
    '''
    r = requests.get(url)
    with open('local.html', 'w') as output_file:
        output_file.write(r.text)


def get_src_and_alt(res, theme):
    if theme == '':
        theme = 'all'
    else:
        theme = 'catalog/' + theme
    url = 'https://wallpaperscraft.com/'+ theme + '/' + res
    print(url)
    get_local(url)

    with open('local.html') as fp:
        soup = BeautifulSoup(fp, 'lxml')

    #Находим все вхождения div с классом wallpaper_pre
    imgs = soup.find_all('div', {'class': 'wallpaper_pre'})

    srcs = []
    #Записываем "сырые" данные о ссылке и описании в srcs
    for img in imgs:
        wall = {}
        wall['src'] = img.find('a').get('href')
        wall['alt'] = img.find('img').get('alt')
        srcs.append(wall)

    #"Чистим" описание от запятых и получаем чистую ссылку на обои
    for src in srcs:
        src['alt'] = re.sub(',', '', src['alt'])
        src['alt'] = re.sub('Preview wallpaper', '', src['alt'])
        src['alt'] = src['alt'].split()

        src['src'] = re.sub('download', 'image', src['src'])
        src['src'] = re.sub('/'+res, '_'+res+'.jpg', src['src'])

    return srcs


res = '1920x1080'
theme = 'cars'
imgs = get_src_and_alt(res, theme)

print(imgs)
