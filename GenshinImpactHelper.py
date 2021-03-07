import ast
import configparser
import csv
import datetime
import os
import re
import sys
import urllib.parse
import urllib.request

import certifi
import urllib3
import ctypes
import locale
from gettext import gettext as _
import gettext

app_lang = locale.getdefaultlocale()

windll = ctypes.windll.kernel32
windll.GetUserDefaultUILanguage()
app_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]

version = '0.4.2-beta'

http = urllib3.PoolManager(ca_certs=certifi.where())
environ_username = os.environ['username']
config = configparser.ConfigParser()

path = os.getcwd()
file_path = r'C:\Users\{}\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt'.format(environ_username)
setting_path = path + '\\settings.ini'

payload = dict()
new_url = 'https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/version'
req = http.request('GET', new_url, fields=payload)
version_download = req.data.decode("UTF-8")

os.environ['LANGUAGE'] = app_lang
gettext.textdomain('GIGH')
gettext.bindtextdomain('GIGH', path + '\\lang')

if version != version_download[:-1]:
    os.system("start {}".format('https://github.com/satan007/genshin-impact-gacha-helper/releases/latest'))
    print(_('New version found. Open Browser'))  # Найдена новая версия. Открываю браузер

print(_('Stage 1. Getting authorization data from a file.'))  # Этап 1. Получение данных авторизации из файла.
if not os.path.exists(file_path) and not os.path.exists(setting_path):  # output_log.txt и settings.ini не найдены
    print(_('No user data files found.'))  # Файлы данных пользователя не найдены.
    input(_('Press Enter to continue...'))
    sys.exit()
elif not os.path.exists(file_path) and os.path.exists(setting_path):  # output_log.txt не найден
    print(_(
        'No current authorization data was found. Are you sure you have discovered the history?'))  # Актуальные данные авторизации не найдены. Вы точно открывали историю молитв?
    print(_(
        'Previously saved data is used. Differences in values are possible.'))  # Используются ранее сохраненные данные. Возможны расхождения значений.
    config.read(setting_path)
    region = config.get('Settings', 'server')
    lang = config.get('Settings', 'lang')
    authkey_ver = config.get('Settings', 'authentication_key_version')
    authkey = config.get('Settings', 'authentication_key')
    gacha_id = config.get('Check', 'last_banner_id')
    init_type = config.get('Check', 'last_banner_code')
    banner_list = []
    banner_list = ast.literal_eval(config.get('Check', 'banner_id_list'))
elif os.path.exists(file_path) and not os.path.exists(setting_path):  # settings.ini не найден
    f = open(file_path, 'r', encoding="utf-8")
    dirty_url = ''
    for line in f:
        if re.search('OnGetWebViewPageFinish:', line):
            if re.search('/log', line):
                dirty_url = str(line)
    f.close()
    if dirty_url != '':
        url = dirty_url[23:-6]
        fragment = urllib.parse.urlparse(url)
        fragments = dict(urllib.parse.parse_qs(fragment.query))
        region = fragments['region'][0]
        lang = fragments['lang'][0]
        authkey_ver = fragments['authkey_ver'][0]
        authkey = fragments['authkey'][0]
        gacha_id = fragments['gacha_id'][0]
        init_type = fragments['init_type'][0]
        banner_list = []
        banner_list.append(gacha_id)
        config.add_section('Settings')
        config.set('Settings', 'server', region)
        config.set('Settings', 'lang', lang)
        config.set('Settings', 'authentication_key_version', authkey_ver)
        config.set('Settings', 'authentication_key', authkey)
        config.add_section('Check')
        config.set('Check', 'last_banner_id', gacha_id)
        config.set('Check', 'last_banner_code', init_type)
        config.set('Check', 'banner_id_list', init_type)
        with open(setting_path, "w") as config_file:
            config.write(config_file)
    else:
        print(_('No user data files found.'))  # Файлы данных пользователя не найдены.
        input(_('Press Enter to continue...'))
        sys.exit()
elif os.path.exists(file_path) and os.path.exists(setting_path):  # оба файла на месте
    f = open(file_path, 'r', encoding="utf-8")
    dirty_url = ''
    try:
        for line in f:
            if re.search('OnGetWebViewPageFinish:', line):
                if re.search('/log', line):
                    dirty_url = str(line)
    except:
        pass
    f.close()
    if dirty_url != '':
        url = dirty_url[23:-6]
        fragment = urllib.parse.urlparse(url)
        fragments = dict(urllib.parse.parse_qs(fragment.query))
        region = fragments['region'][0]
        lang = fragments['lang'][0]
        authkey_ver = fragments['authkey_ver'][0]
        authkey = fragments['authkey'][0]
        gacha_id = fragments['gacha_id'][0]
        init_type = fragments['init_type'][0]
        config.read(setting_path)
        banner_list_old = []
        banner_list = []
        banner_list_old = ast.literal_eval(config.get('Check', 'banner_id_list'))
        banner_list_old.append(gacha_id)
        for i in banner_list_old:
            if i not in banner_list:
                banner_list.append(i)
        config.set('Settings', 'server', region)
        config.set('Settings', 'lang', lang)
        config.set('Settings', 'authentication_key_version', authkey_ver)
        config.set('Settings', 'authentication_key', authkey)
        config.set('Check', 'last_banner_id', gacha_id)
        config.set('Check', 'last_banner_code', init_type)
        config.set('Check', 'banner_id_list', str(banner_list))
        with open(setting_path, "w") as config_file:
            config.write(config_file)
    else:
        print(_(
            'No current authorization data was found. Are you sure you have discovered the history?'))  # Актуальные данные авторизации не найдены. Вы точно открывали историю молитв?
        print(_(
            'Previously saved data is used. Differences in values are possible.'))  # Используются ранее сохраненные данные. Возможны расхождения значений.
        config.read(setting_path)
        region = config.get('Settings', 'server')
        lang = config.get('Settings', 'lang')
        authkey_ver = config.get('Settings', 'authentication_key_version')
        authkey = config.get('Settings', 'authentication_key')
        gacha_id = config.get('Check', 'last_banner_id')
        init_type = config.get('Check', 'last_banner_code')
        banner_list = []
        banner_list = ast.literal_eval(config.get('Check', 'banner_id_list'))


def download_file(url, save_path):
    print(_('Starting download {download_url}'.format(download_url=url)))
    try:
        urllib.request.urlretrieve(url, save_path)
    except:
        print(_("Can't download file {download_url}".format(download_url=url)))
        print(_('Create empty file'))
        file = open(save_path, 'w', encoding="utf-8")
        file.close()
    pass
    print(_('File uploaded successfully in {directory}'.format(directory=save_path)))


def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        if not os.path.exists(path):
            print(_('Failed to create directory'))
    pass


gacha_path = path + '\\' + 'gacha'

create_directory(gacha_path)
create_directory('{}\\{}'.format(gacha_path, region))

if not os.path.exists(gacha_path + '\\' + 'gacha_custom_code_list'):
    f = open(gacha_path + '\\' + 'gacha_custom_code_list', 'w', encoding='utf-8')
    f.close()
f = open(gacha_path + '\\' + 'gacha_custom_code_list', 'r', encoding='utf-8')

print(_('Stage 2. Download the History.'))  # Этап 2. Получение истории молитв.

lang_dict = {
    'en': "en-us",
    'fr': "fr-fr",
    'de': "de-de",
    'es': "es-es",
    'pt': "pt-pt",
    'ru': "ru-ru",
    'ja': "ja-jp",
    'ko': "ko-kr",
    'th': "th-th",
    'vi': "vi-vn",
    'id': "id-id",
    'tc': "zh-tw",
    'sc': "zh-cn"
}
gacha_code = {'en-us': [{'key': '200', 'name': 'Permanent Wish'}, {'key': '100', 'name': 'Novice Wishes'},
                        {'key': '301', 'name': 'Character Event Wish'}, {'key': "302", 'name': "Weapon Event Wish"}],
              'fr-fr': [{'key': "200", 'name': "Vœux permanents"}, {'key': "100", 'name': "Vœux des débutants"},
                        {'key': "301", 'name': "Vœux événements de personnage"},
                        {'key': "302", 'name': "Vœux événements d'arme"}],
              "de-de": [{'key': "200", 'name': "Standardgebet"}, {'key': "100", 'name': "Neulingsgebete"},
                        {'key': "301", 'name': "Figurenaktionsgebet"}, {'key': "302", 'name': "Waffenaktionsgebet"}],
              "es-es": [{'key': "200", 'name': "Gachapón permanente"},
                        {'key': "100", 'name': "Gachapón de principiante"},
                        {'key': "301", 'name': "Gachapón promocional de personaje"},
                        {'key': "302", 'name': "Gachapón promocional de arma"}],
              "pt-pt": [{'key': "200", 'name': "Desejo Comum"}, {'key': "100", 'name': "Desejos de Novato"},
                        {'key': "301", 'name': "Oração do Evento do Personagem"},
                        {'key': "302", 'name': "Oração do Evento de Arma"}],
              "ru-ru": [{'key': "200", 'name': "Стандартная молитва"}, {'key': "100", 'name': "Молитва новичка"},
                        {'key': "301", 'name': "Молитва события персонажа"},
                        {'key': "302", 'name': "Молитва события оружия"}],
              "ja-jp": [{'key': "200", 'name': "通常祈願"}, {'key': "100", 'name': "初心者向け祈願"},
                        {'key': "301", 'name': "イベント祈願・キャラクター"}, {'key': "302", 'name': "イベント祈願・武器"}],
              "ko-kr": [{'key': "200", 'name': "상주 기원"}, {'key': "100", 'name': "초심자 기원"},
                        {'key': "301", 'name': "캐릭터 이벤트 기원"}, {'key': "302", 'name': "무기 이벤트 기원"}],
              "th-th": [{'key': "200", 'name': "อธิษฐานถาวร"}, {'key': "100", 'name': "ผู้เริ่มอธิษฐาน"},
                        {'key': "301", 'name': "กิจกรรมอธิษฐานตัวละคร"}, {'key': "302", 'name': "กิจกรรมอธิษฐานอาวุธ"}],
              "vi-vn": [{'key': "200", 'name': "Cầu Nguyện Thường"}, {'key': "100", 'name': "Cầu Nguyện Tân Thủ"},
                        {'key': "301", 'name': "Cầu Nguyện Nhân Vật"}, {'key': "302", 'name': "Cầu Nguyện Vũ Khí"}],
              "id-id": [{'key': "200", 'name': "Standard Wish"}, {'key': "100", 'name': "Permohonan Pemula"},
                        {'key': "301", 'name': "Event Permohonan Karakter"},
                        {'key': "302", 'name': "Event Permohonan Senjata"}],
              "zh-cn": [{'key': "200", 'name': "常驻祈愿"}, {'key': "100", 'name': "新手祈愿"},
                        {'key': "301", 'name': "角色活动祈愿"}, {'key': "302", 'name': "武器活动祈愿"}],
              "zh-tw": [{'key': "200", 'name': "常駐祈願"}, {'key': "100", 'name': "新手祈願"},
                        {'key': "301", 'name': "角色活動祈願"}, {'key': "302", 'name': "武器活動祈願"}]}
lang = lang_dict[lang]
for gacha in gacha_code[lang]:
    while_end = 0
    page = 1
    path_gacha_log = ''
    array = []
    while while_end == 0:
        payload = dict(authkey_ver=authkey_ver, region=region, init_type=init_type, lang=lang, authkey=authkey,
                       gacha_type=gacha['key'], page=page, size='20')
        new_url = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog'
        req = http.request('GET', new_url, fields=payload)
        dict_str = req.data.decode("UTF-8")
        try:
            my_data = ast.literal_eval(dict_str)
        except:
            print(_(
                'Error in authorization data. Open the history and restart the program.'))  # Ошибка в данных авторизации. Откройте историю молитв и перезапустите программу.
            input(_("Press Enter to continue..."))
            sys.exit()
        if not my_data['data']['list']:
            while_end = 1
        else:
            for item_list in my_data['data']['list']:
                array.append([item_list['item_id'], item_list['time'], item_list['name'], item_list['item_type'],
                              item_list['rank_type']])
            user_id = my_data['data']['list'][0]['uid']
            path_gacha_log = gacha_path + '\\' + region + '\\' + user_id
            create_directory(path_gacha_log)
        page = page + 1
    if path_gacha_log != '':
        f = open(path_gacha_log + '\\' + gacha['key'] + '.csv', 'w', encoding="utf-8")
        for i in array:
            if i[0] == '':
                i[0] = '0'
            f.write(i[0] + ',' + i[1] + ',' + i[2] + ',' + i[3] + ',' + i[4] + '\n')
        f.close()

items_path = path + '\\' + 'items'

create_directory(items_path + '\\' + region)
create_directory(items_path + '\\' + region + '\\' + lang)

print(_('Stage 2.1. Downloading translations.'))  # Этап 2.1. Получение переводов для разных языков
download_file('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/banner_code_list',
              path + '\\' + 'banner_code_list')

try:
    banner_code_list = open(path + '\\' + 'banner_code_list', 'r', encoding="utf-8")
    for g in banner_code_list:
        if g[:-1] not in banner_list:
            banner_list.append(g[:-1])
    banner_code_list.close()
except:
    print(_('Not found {path}'.format(path=path + '\\banner_code_list')))
banner_list.sort()
banner_code_list = open(path + '\\' + 'banner_code_list', 'w', encoding="utf-8")
for g in banner_list:
    banner_code_list.write(g + '\n')
banner_code_list.close()
star_5 = []
star_4 = []
star_3 = []
star_5_old = []
star_4_old = []
star_3_old = []
download_file(
    'https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/{}/{}/star_3.csv'.format(region,
                                                                                                                lang),
    items_path + '\\' + region + '\\' + lang + '\\' + 'star_3_download.csv')
download_file(
    'https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/{}/{}/star_4.csv'.format(region,
                                                                                                                lang),
    items_path + '\\' + region + '\\' + lang + '\\' + 'star_4_download.csv')
download_file(
    'https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/{}/{}/star_5.csv'.format(region,
                                                                                                                lang),
    items_path + '\\' + region + '\\' + lang + '\\' + 'star_5_download.csv')
try:
    f = open(path + '\\items\\' + region + '\\' + lang + '\\star_5.csv', 'r', encoding="utf-8")
    star_5_old = list(csv.reader(f))
    f.close()
    f = open(path + '\\items\\' + region + '\\' + lang + '\\star_3.csv', 'r', encoding="utf-8")
    star_3_old = list(csv.reader(f))
    f.close()
    f = open(path + '\\items\\' + region + '\\' + lang + '\\star_4.csv', 'r', encoding="utf-8")
    star_4_old = list(csv.reader(f))
    f.close()
except:
    f = open(path + '\\items\\' + region + '\\' + lang + '\\star_5.csv', 'w', encoding="utf-8")
    f.close()
    f = open(path + '\\items\\' + region + '\\' + lang + '\\star_3.csv', 'w', encoding="utf-8")
    f.close()
    f = open(path + '\\items\\' + region + '\\' + lang + '\\star_4.csv', 'w', encoding="utf-8")
    f.close()
f = open(path + '\\items\\' + region + '\\' + lang + '\\star_5_download.csv', 'r', encoding="utf-8")
star_5_old = star_5_old + list(csv.reader(f))
f.close()
f = open(path + '\\items\\' + region + '\\' + lang + '\\star_3_download.csv', 'r', encoding="utf-8")
star_3_old = star_3_old + list(csv.reader(f))
f.close()
f = open(path + '\\items\\' + region + '\\' + lang + '\\star_4_download.csv', 'r', encoding="utf-8")
star_4_old = star_4_old + list(csv.reader(f))
f.close()

items_request = http.request('GET',
                             'https://webstatic-sea.mihoyo.com/hk4e/gacha_info/%s/%s/%s.json' % (region, 'items', lang))
if items_request.status == 200:
    items = items_request.data.decode("UTF-8")
    items = ast.literal_eval(items)
    for item in items:
        if item['rank_type'] == '5':
            star_5_old.append([str(item['item_id']), item['item_type'], item['name'], '', ''])
        elif item['rank_type'] == '4':
            star_4_old.append([str(item['item_id']), item['item_type'], item['name'], '', ''])
        elif item['rank_type'] == '3':
            star_3_old.append([str(item['item_id']), item['item_type'], item['name'], '', ''])
for i in banner_list:
    items_request = http.request('GET', 'https://webstatic-sea.mihoyo.com/hk4e/gacha_info/%s/%s/%s.json' % (
        region, i, lang))
    if items_request.status == 200:
        items = items_request.data.decode("UTF-8")
        items = ast.literal_eval(items)
        for item in items.get('r5_up_items'):
            star_5_old.append(
                [str(item.get('item_id')), item.get('item_type'), item.get('item_name'),
                 item.get('item_img', '').replace("\\", ""),
                 item.get('item_attr', '')])
        for item in items.get('r4_up_items'):
            star_4_old.append(
                [str(item.get('item_id')), item.get('item_type'), item.get('item_name'),
                 item.get('item_img', '').replace("\\", ""),
                 item.get('item_attr', '')])

star_5_old = sorted(star_5_old)
star_4_old = sorted(star_4_old)
star_3_old = sorted(star_3_old)
for i in star_5_old:
    if i not in star_5:
        star_5.append(i)
for i in star_4_old:
    if i not in star_4:
        star_4.append(i)
for i in star_3_old:
    if i not in star_3:
        star_3.append(i)

f = open(path + '\\items\\' + region + '\\' + lang + '\\star_5.csv', 'w', encoding="utf-8")
for l in star_5:
    try:
        f.write(str(l[0]) + ',' + str(l[1]) + ',' + str(l[2]) + ',' + str(l[3]) + ',' + str(l[4]) + '\n')
    except:
        print('Неверный формат строки: {}'.format(l))
f.close()
f = open(path + '\\items\\' + region + '\\' + lang + '\\star_4.csv', 'w', encoding="utf-8")
for l in star_4:
    try:
        f.write(str(l[0]) + ',' + str(l[1]) + ',' + str(l[2]) + ',' + str(l[3]) + ',' + str(l[4]) + '\n')
    except:
        print('Неверный формат строки: {}'.format(l))
f.close()
f = open(path + '\\items\\' + region + '\\' + lang + '\\star_3.csv', 'w', encoding="utf-8")
for l in star_3:
    try:
        f.write(str(l[0]) + ',' + str(l[1]) + ',' + str(l[2]) + ',' + str(l[3]) + ',' + str(l[4]) + '\n')
    except:
        print('Неверный формат строки: {}'.format(l))
f.close()

# Шаг №3. Получение сохраненных ранее данных и расчет вероятности

gacha_dict = {}
gacha_percent = {}
s5_index = []
s4_index = []
s3_index = []
s5_index_name = []
s4_index_name = []

star_5 = open(path + '\\items\\' + region + '\\' + lang + '\\star_5.csv', 'r', encoding="utf-8")
s5 = list(csv.reader(star_5))
star_5.close()
star_4 = open(path + '\\items\\' + region + '\\' + lang + '\\star_4.csv', 'r', encoding="utf-8")
s4 = list(csv.reader(star_4))
star_4.close()
star_3 = open(path + '\\items\\' + region + '\\' + lang + '\\star_3.csv', 'r', encoding="utf-8")
s3 = list(csv.reader(star_3))
star_3.close()

for i in s5:
    s5_index.append(i[0])
    s5_index_name.append(i[2])
for i in s4:
    s4_index.append(i[0])
    s4_index_name.append(i[2])
for i in s3:
    s3_index.append(i[0])

print('Этап 3. Расчет вероятности молитв')
for gacha in gacha_code[lang]:
    gacha_translated = open(gacha_path + '\\' + region + '\\' + user_id + '\\' + 'end_%s.csv' % gacha['key'], 'w',
                            encoding='utf-8')
    try:
        f = open(gacha_path + '\\' + region + '\\' + user_id + '\\' + gacha['key'] + '.csv', 'r', encoding="utf-8")
        gacha_dict[gacha['key']] = list(csv.reader(f))
    except:
        print('Файл {} не найден'.format(gacha_path + '\\' + region + '\\' + user_id + '\\' + gacha['key'] + '.csv'))
        gacha_dict[gacha['key']] = list('')

    # print(len(gacha_dict[gacha]))
    for i in range(len(gacha_dict[gacha['key']])):
        if gacha_dict[gacha['key']][i][0] in s3_index:
            index = s3_index.index(gacha_dict[gacha['key']][i][0])
            gacha_dict[gacha['key']][i].append(s3[index][2])
            gacha_dict[gacha['key']][i].append(s3[index][1])
            gacha_dict[gacha['key']][i].append('3')
            gacha_dict[gacha['key']][i].append(s3[index][3])
        elif gacha_dict[gacha['key']][i][0] in s4_index:
            index = s4_index.index(gacha_dict[gacha['key']][i][0])
            gacha_dict[gacha['key']][i].append(s4[index][2])
            gacha_dict[gacha['key']][i].append(s4[index][1])
            gacha_dict[gacha['key']][i].append('4')
            gacha_dict[gacha['key']][i].append(s4[index][3])
        elif gacha_dict[gacha['key']][i][0] in s5_index:
            index = s5_index.index(gacha_dict[gacha['key']][i][0])
            gacha_dict[gacha['key']][i].append(s5[index][2])
            gacha_dict[gacha['key']][i].append(s5[index][1])
            gacha_dict[gacha['key']][i].append('5')
            gacha_dict[gacha['key']][i].append(s5[index][3])

    gacha_dict[gacha['key']].reverse()
    s4_percent = 0, 0
    s5_percent = 0, 0
    s4_count = 1
    s5_count = 1
    s3_count = -1
    count = 0
    gacha_img = ''
    graph = '<div><div class="row"><div class="col"><table bordercolor="#fa8e47" border style="width: 100%;"><tbody><tr>'
    for i in gacha_dict[gacha['key']]:
        if i[0] == '0':
            if i[4] == '4':
                index = s4_index_name.index(i[2])
                i[0] = s4[index][0]
                i.append(s4[index][3])
            if i[4] == '5':
                index = s5_index_name.index(i[2])
                i[0] = s5[index][0]
                i.append(s5[index][3])
        s4_count = s4_count + 1
        s5_count = s5_count + 1
        s3_count = s3_count + 1
        if count % 40 == 0:
            graph = graph + '</tr><tr>'
        count = count + 1
        f = open(path + '\\assets\\img_block.html', 'r', encoding="utf-8")
        img_block = f.read()
        f.close()
        if i[4] == '4':
            if i[5] == '':
                gacha_img = gacha_img + img_block.format(
                    'items/img/' + i[0] + '.png', i[2])
            else:
                gacha_img = gacha_img + img_block.format(
                    i[5], i[2])
            s4_count = 1
            s3_count = -1
            graph = graph + '<td style="background-color: #9c27b0;height: 25px;"></td>'
        elif i[4] == '5':
            if i[5] == '':
                gacha_img = gacha_img + img_block.format(
                    'items/img/' + i[0] + '.png', i[2])
            else:
                gacha_img = gacha_img + img_block.format(
                    i[5], i[2])
            s5_count = 1
            s3_count = -1
            graph = graph + '<td style="background-color: gold;height: 25px;"></td>'
        elif i[4] == '3':
            graph = graph + '<td style="background-color: #007bff;height: 25px;"></td>'
        elif i[4] == '-1':
            gacha_img = gacha_img + '<img style="width: 20%; border-radius: 0 0 25% 0;" src="items/img/{}.png" />'.format(
                i[0])

        gacha_translated.write(i[2] + ',' + i[1] + ',' + i[3] + ',' + i[4] + '\n')

    if gacha['key'] == '302':
        s5_percent = (1 - ((1 - 0.007) ** s5_count)) * 100
        s4_percent = (1 - ((1 - 0.060) ** s4_count)) * 100
        if s5_count == 80:
            s5_percent = 100.0
        if s4_count == 10:
            s4_percent = 100.0
            s5_percent = 0.7
    else:
        s5_percent = (1 - ((1 - 0.006) ** s5_count)) * 100
        s4_percent = (1 - ((1 - 0.051) ** s4_count)) * 100
        if s5_count == 90:
            s5_percent = 100.0
        if s4_count == 10:
            s4_percent = 100.0
            s5_percent = 0.6
    graph = graph + '</tr></tbody></table></div></div></div>'
    gacha_percent[gacha['key']] = {'star_4': s4_percent, 'star_5': s5_percent, 'star_4_count': s4_count,
                                   'star_5_count': s5_count, 'img': gacha_img, 'count': count,
                                   'graph': graph}
    gacha_translated.close()

f = open(path + '\\assets\\page.html', 'r', encoding="utf-8")
html_page = f.read()
f.close()
html_page_format = {}
for gacha in gacha_code[lang]:
    html_page_format[gacha['key']] = gacha['name']
html_page = html_page.format(
    head_100=str('{}({})'.format(html_page_format['100'], gacha_percent['100']['count'])),
    star_4_percent_100=str(round(gacha_percent['100']['star_4'])),
    star_4_percent_100_text=str(round(gacha_percent['100']['star_4'], 3)),
    star_5_percent_100=str(round(gacha_percent['100']['star_5'])),
    star_5_percent_100_text=str(round(gacha_percent['100']['star_5'], 3)),
    star_4_100=str(gacha_percent['100']['star_4_count']) + r'\10',
    star_5_100=str(gacha_percent['100']['star_5_count']) + r'\90',
    img_100=str(gacha_percent['100']['img']) + str(gacha_percent['100']['graph']),
    head_200=str('{}({})'.format(html_page_format['200'], gacha_percent['200']['count'])),
    star_4_percent_200=str(round(gacha_percent['200']['star_4'])),
    star_4_percent_200_text=str(round(gacha_percent['200']['star_4'], 3)),
    star_5_percent_200=str(round(gacha_percent['200']['star_5'])),
    star_5_percent_200_text=str(round(gacha_percent['200']['star_5'], 3)),
    star_4_200=str(gacha_percent['200']['star_4_count']) + r'\10',
    star_5_200=str(gacha_percent['200']['star_5_count']) + r'\90',
    img_200=str(gacha_percent['200']['img']) + str(gacha_percent['200']['graph']),
    head_301=str('{}({})'.format(html_page_format['301'], gacha_percent['301']['count'])),
    star_4_percent_301=str(round(gacha_percent['301']['star_4'])),
    star_4_percent_301_text=str(round(gacha_percent['301']['star_4'], 3)),
    star_5_percent_301=str(round(gacha_percent['301']['star_5'])),
    star_5_percent_301_text=str(round(gacha_percent['301']['star_5'], 3)),
    star_4_301=str(gacha_percent['301']['star_4_count']) + r'\10',
    star_5_301=str(gacha_percent['301']['star_5_count']) + r'\90',
    img_301=str(gacha_percent['301']['img']) + str(gacha_percent['301']['graph']),
    head_302=str('{}({})'.format(html_page_format['302'], gacha_percent['302']['count'])),
    star_4_percent_302=str(round(gacha_percent['302']['star_4'])),
    star_4_percent_302_text=str(round(gacha_percent['302']['star_4'], 3)),
    star_5_percent_302=str(round(gacha_percent['302']['star_5'])),
    star_5_percent_302_text=str(round(gacha_percent['302']['star_5'], 3)),
    star_4_302=str(gacha_percent['302']['star_4_count']) + r'\10',
    star_5_302=str(gacha_percent['302']['star_5_count']) + r'\80',
    img_302=str(gacha_percent['302']['img']) + str(gacha_percent['302']['graph']))
now_time = datetime.datetime.now()
print('Формирование странички с результатом. {html_path}'.format(
    html_path=path + '\\' + now_time.strftime("%Y_%m_%d-%H_%M_%S") + '.html'))
f = open(path + '\\' + now_time.strftime("%Y_%m_%d-%H_%M_%S") + '.html', 'w', encoding='utf-8')
f.write(str(html_page))
f.close()
html_path = os.path.abspath(path + '\\' + now_time.strftime("%Y_%m_%d-%H_%M_%S") + '.html')
sys.stdout = os.devnull
sys.stderr = os.devnull
os.system("start {}".format(html_path))
