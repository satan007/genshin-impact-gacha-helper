import os
import re
import sys
import urllib.request, urllib.parse
import urllib3
import certifi
import ast
import csv
import configparser

http = urllib3.PoolManager(ca_certs=certifi.where())
environ_username = os.environ['username']
config = configparser.ConfigParser()

path = os.getcwd()
file_path = r'C:\Users\%s\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt' % (environ_username) 
setting_path = path+'\\settings.ini'

print('Этап 1. Получение данных авторизации из файла.')
if not os.path.exists(file_path) and not os.path.exists(setting_path): #output_log.txt и settings.ini не найдены
    print('Файлы данных пользователя не найдены.')
    input("Press Enter to continue...")
    sys.exit()
elif not os.path.exists(file_path) and os.path.exists(setting_path): #output_log.txt не найден
    print('Актуальные данные авторизации не найдены. Вы точно открывали историю молитв?')
    print('Используются ранее сохраненные данные. Возможны расхождения значений.')
    config.read(setting_path)
    region = config.get('Settings','server')
    lang = config.get('Settings','lang')
    authkey_ver = config.get('Settings','authentication_ley_version')
    authkey = config.get('Settings','authentication_key')
    gacha_id = config.get('Check','last_banner_id')
    init_type = config.get('Check','last_banner_code')
elif os.path.exists(file_path) and not os.path.exists(setting_path): #settings.ini не найден
    f = open (file_path,'r', encoding="utf-8")
    dirty_url=''
    for line in f:
        if re.search('OnGetWebViewPageFinish:',line):
            if re.search('/log',line):
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
        config.add_section('Settings')
        config.set('Settings','server',region)
        config.set('Settings','lang',lang)
        config.set('Settings','authentication_key_version',authkey_ver)
        config.set('Settings','authentication_key',authkey)
        config.add_section('Check')
        config.set('Check','last_banner_id',gacha_id)
        config.set('Check','last_banner_code',init_type)
        with open(setting_path, "w") as config_file:
            config.write(config_file)
    else:
        print('Файлы данных пользователя не найдены.')
        input("Press Enter to continue...")
        sys.exit()
elif os.path.exists(file_path) and os.path.exists(setting_path): #оба файла на месте
    f = open (file_path,'r', encoding="utf-8")
    dirty_url=''
    try:
        for line in f:
            if re.search('OnGetWebViewPageFinish:',line):
                if re.search('/log',line):
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
        config.add_section('Settings')
        config.set('Settings','server',region)
        config.set('Settings','lang',lang)
        config.set('Settings','authentication_key_version',authkey_ver)
        config.set('Settings','authentication_key',authkey)
        config.add_section('Check')
        config.set('Check','last_banner_id',gacha_id)
        config.set('Check','last_banner_code',init_type)
        with open(setting_path, "w") as config_file:
            config.write(config_file)
    else:
        print('Актуальные данные авторизации не найдены. Вы точно открывали историю молитв?')
        print('Используются ранее сохраненные данные. Возможны расхождения значений.')
        config.read(setting_path)
        region = config.get('Settings','server')
        lang = config.get('Settings','lang')
        authkey_ver = config.get('Settings','authentication_key_version')
        authkey = config.get('Settings','authentication_key')
        gacha_id = config.get('Check','last_banner_id')
        init_type = config.get('Check','last_banner_code')

def download_file(url,save_path):
    print('Начинаю загрузку {}'.format(url))
    try: 
        urllib.request.urlretrieve(url, save_path)
    except:
        print ("Не могу загрузить файл {}".format(url))
        print ("Создаю пустой файл")
        f = open(save_path,'w', encoding="utf-8")
        f.close()
    pass
def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        if not os.path.exists(path):
            print ("Создать директорию не удалось")
    pass



gacha_path = path + '\\' + 'gacha'

create_directory(gacha_path)
create_directory(gacha_path+'\\'+region)


if not os.path.exists(gacha_path+'\\'+'gacha_custom_code_list'):
    f = open(gacha_path+'\\'+'gacha_custom_code_list', 'w', encoding='utf-8')
    f.close()
f = open(gacha_path+'\\'+'gacha_custom_code_list', 'r', encoding='utf-8')

print('Этап 2. Получение истории молитв.')
download_file('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_code_list', gacha_path + '\\' + 'gacha_code_list')

gacha_code=[]
try:
    gacha_code_file = open(gacha_path+'\\'+'gacha_code_list', 'r', encoding="utf-8")
    for g in gacha_code_file:
        gacha_code.append(g[:-1])
    gacha_code_file.close()
except:
    print ("Не могу найти файл %s\gacha_code_list" % gacha_path)
for g in f:
    gacha_code.append(g[:-1])

f.close()
if init_type not in gacha_code:
    gacha_code.append(init_type)
    f = open(gacha_path+'\\'+'gacha_custom_code_list', 'a', encoding='utf-8')
    f.write(init_type+'\n')
    f.close()
gacha_code = [line.rstrip() for line in gacha_code]
for gacha in gacha_code:
    while_end = 0
    page = 1
    path_gacha_log = ''
    array = []
    while while_end == 0:
        payload = {'authkey_ver':authkey_ver, 'region':region, 'authkey':authkey,'gacha_type':gacha, 'page':page, 'size':'20'}
        newurl = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog' 
        req = http.request('GET', newurl, fields=payload)
        dict_str = req.data.decode("UTF-8")
        try:
            mydata = ast.literal_eval(dict_str)
        except:
            print('\nОшибка в данных авторизации. Откройте историю молитв и перезапустите программу.')
            input("Press Enter to continue...")
            sys.exit()
        if mydata['data']['list'] == []:
            while_end = 1
        else:
            for item_list in mydata['data']['list']:
                array.append([item_list['item_id'],item_list['time']])
            user_id = mydata['data']['list'][0]['uid']
            path_gacha_log = gacha_path+'\\'+region+'\\'+user_id
            create_directory(path_gacha_log)
        page = page + 1
    if path_gacha_log != '':
        f = open(path_gacha_log+'\\'+gacha+'.csv', 'w', encoding="utf-8")
        for i in array:
            f.write(i[0]+','+i[1]+'\n')
        f.close()

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

lang=lang_dict[lang]
items_path = path+'\\'+'items'


create_directory(items_path+'\\'+region)
create_directory(items_path+'\\'+region+'\\'+lang)


print('Этап 2.1. Получение переводов для разных языков')

star_5 = []
star_4 = []
star_3 = []
download_file('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/{}/{}/star_3.csv'.format(region, lang), items_path+'\\'+region+'\\'+lang+'\\'+'star_3.csv')
download_file('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/{}/{}/star_4.csv'.format(region, lang), items_path+'\\'+region+'\\'+lang+'\\'+'star_4.csv')
download_file('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/{}/{}/star_5.csv'.format(region, lang), items_path+'\\'+region+'\\'+lang+'\\'+'star_5.csv')

f = open(path+'\\items\\'+region+'\\'+lang+'\\star_5.csv','r', encoding="utf-8")
star_5_old = list(csv.reader(f))
f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_3.csv','r', encoding="utf-8")
star_3_old = list(csv.reader(f))
f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_4.csv','r', encoding="utf-8")
star_4_old = list(csv.reader(f))
f.close()


items_request = http.request('GET', 'https://webstatic-sea.mihoyo.com/hk4e/gacha_info/%s/%s/%s.json'%(region,'items',lang))
if items_request.status == 200:
    items = items_request.data.decode("UTF-8")
    items = ast.literal_eval(items)
    for item in items:
        if item['rank_type']=='5':
            star_5_old.append([str(item['item_id']),item['item_type'],item['name']])
        elif item['rank_type']=='4':
            star_4_old.append([str(item['item_id']),item['item_type'],item['name']])
        elif item['rank_type']=='3':
            star_3_old.append([str(item['item_id']),item['item_type'],item['name']])

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

f = open(path+'\\items\\'+region+'\\'+lang+'\\star_5.csv','w', encoding="utf-8")
for l in star_5:
    f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_4.csv','w', encoding="utf-8")
for l in star_4:
    f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_3.csv','w', encoding="utf-8")
for l in star_3:
    f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
f.close()

#Шаг №3. Получение сохранненых ранее данных и расчет вероятности

gacha_dict={}
gacha_percent={}
s5_index=[]
s4_index=[]
s3_index=[]


star_5 = open (path+'\\items\\'+region+'\\'+lang+'\\star_5.csv','r', encoding="utf-8")
s5=list(csv.reader(star_5))
star_5.close()
star_4 = open (path+'\\items\\'+region+'\\'+lang+'\\star_4.csv','r', encoding="utf-8")
s4=list(csv.reader(star_4))
star_4.close()
star_3 = open (path+'\\items\\'+region+'\\'+lang+'\\star_3.csv','r', encoding="utf-8")
s3=list(csv.reader(star_3))
star_3.close()

for i in s5:
    s5_index.append(i[0])
for i in s4:
    s4_index.append(i[0])
for i in s3:
    s3_index.append(i[0])


print('Этап 3. Расчет вероятности молитв')
for gacha in ['100','200','301','302']:
    gacha_translated=open(gacha_path+'\\'+region+'\\'+user_id+'\\'+'end_%s.csv' % gacha,'w',encoding='utf-8')
    try:
        f = open(gacha_path+'\\'+region+'\\'+user_id+'\\'+gacha+'.csv', 'r', encoding="utf-8")
    except:
        print('Файл не найден')
    gacha_dict[gacha]=list(csv.reader(f))
    #print(len(gacha_dict[gacha]))
    for i in range(len(gacha_dict[gacha])):
        if gacha_dict[gacha][i][0] in s3_index:
            index = s3_index.index(gacha_dict[gacha][i][0])
            gacha_dict[gacha][i].append(s3[index][2])
            gacha_dict[gacha][i].append(s3[index][1])
            gacha_dict[gacha][i].append('3')
        elif gacha_dict[gacha][i][0] in s4_index:
            index = s4_index.index(gacha_dict[gacha][i][0])
            gacha_dict[gacha][i].append(s4[index][2])
            gacha_dict[gacha][i].append(s4[index][1])
            gacha_dict[gacha][i].append('4')
        elif gacha_dict[gacha][i][0] in s5_index:
            index = s5_index.index(gacha_dict[gacha][i][0])
            gacha_dict[gacha][i].append(s5[index][2])
            gacha_dict[gacha][i].append(s5[index][1])
            gacha_dict[gacha][i].append('5')
        else:
            gacha_dict[gacha][i].append('')
            gacha_dict[gacha][i].append('')
            gacha_dict[gacha][i].append('-1')
    gacha_dict[gacha].reverse()
    s4_percent = 0,0
    s5_percent = 0,0
    s4_count = 1
    s5_count = 1
    s3_count = -1
    gacha_img=''
    for i in gacha_dict[gacha]:
        s4_count=s4_count+1
        s5_count=s5_count+1
        s3_count = s3_count+1
        if i[4]=='4':
            gacha_img=gacha_img+'<div class="text-center" style="display: inline-flex;background-color: #E9E5DC;border-radius: 5%;    margin: 1%;"><table style="margin: -1px;"><tbody><tr><td><img style="border-radius: 5% 5% 25% 0;" src="items/img/{}.png"></td></tr><tr><td><div class="font-weight-bold font-italic" style="text-overflow: ellipsis;width: 100px;white-space: nowrap;overflow: hidden;">{}</div></td></tr></tbody></table></div>'.format(i[0],i[2])
            s4_count = 1
            s3_count = -1
        elif i[4]=='5':
            gacha_img=gacha_img+'<div class="text-center" style="display: inline-flex;background-color: #E9E5DC;border-radius: 5%;    margin: 1%;"><table style="margin: -1px;"><tbody><tr><td><img style="border-radius: 5% 5% 25% 0;" src="items/img/{}.png"></td></tr><tr><td><div class="font-weight-bold font-italic" style="text-overflow: ellipsis;width: 100px;white-space: nowrap;overflow: hidden;">{}</div></td></tr></tbody></table></div>'.format(i[0],i[2])
            s5_count = 1
            s3_count = -1
        elif i[4]=='-1':
            gacha_img=gacha_img+'<img style="width: 20%; border-radius: 0 0 25% 0;" src="items/img/{}.png" />'.format(i[0])
            
        gacha_translated.write(i[2]+','+i[1]+','+i[3]+','+i[4]+'\n')

    
    if gacha=='302':
        s5_percent=(1-((1-0.007)**s5_count))*100
        s4_percent=(1-((1-0.060)**s4_count))*100
        if s5_count == 80:
            s5_percent=100.0
        if s4_count==10:
            s5_percent=0.7
    else:
        s5_percent=(1-((1-0.006)**s5_count))*100
        s4_percent=(1-((1-0.051)**s4_count))*100
        if s5_count == 90:
            s5_percent=100.0
        if s4_count==10:
            s4_percent=100.0
            s5_percent=0.6
    gacha_percent[gacha]={'star_4':s4_percent,'star_5':s5_percent,'star_4_count':s4_count,'star_5_count':s5_count,'img':gacha_img,'count':len(gacha_dict[gacha])}
    gacha_translated.close()

html_page = '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no"><title>Untitled</title><link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css"><link rel="stylesheet" href="assets/css/styles.min.css"></head><body style="background-color: #333333;"><div class="container-fluid"><div class="row"><div class="col-lg-12 text-center mx-auto mb-5 text-white"><h1 class="display-4 text-white">Genshin Impact Gacha Helper</h1></div></div><div class="row"><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Молитва новичка({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div></div><div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Стандартная молитва({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div></div><div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div></div><div class="row"><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Молитва события персонажа({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div></div><div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Молитва события оружия({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\80</h4></div></div></div><div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div></div><span></span></div><script src="assets/js/jquery.min.js"></script><script src="assets/bootstrap/js/bootstrap.min.js"></script><script src="assets/js/script.min.js"></script></body></html>'.format(str(gacha_percent['100']['count']),str(round(gacha_percent['100']['star_4'])),str(round(gacha_percent['100']['star_4'],3)),str(round(gacha_percent['100']['star_5'])),str(round(gacha_percent['100']['star_5'],3)),str(gacha_percent['100']['star_4_count']),str(gacha_percent['100']['star_5_count']),str(gacha_percent['100']['img']),str(gacha_percent['200']['count']),str(round(gacha_percent['200']['star_4'])),str(round(gacha_percent['200']['star_4'],3)),str(round(gacha_percent['200']['star_5'])),str(round(gacha_percent['200']['star_5'],3)),str(gacha_percent['200']['star_4_count']),str(gacha_percent['200']['star_5_count']),str(gacha_percent['200']['img']),str(gacha_percent['301']['count']),str(round(gacha_percent['301']['star_4'])),str(round(gacha_percent['301']['star_4'],3)),str(round(gacha_percent['301']['star_5'])),str(round(gacha_percent['301']['star_5'],3)),str(gacha_percent['301']['star_4_count']),str(gacha_percent['301']['star_5_count']),str(gacha_percent['301']['img']),str(gacha_percent['302']['count']),str(round(gacha_percent['302']['star_4'])),str(round(gacha_percent['302']['star_4'],3)),str(round(gacha_percent['302']['star_5'])),str(round(gacha_percent['302']['star_5'],3)),str(gacha_percent['302']['star_4_count']),str(gacha_percent['302']['star_5_count']),str(gacha_percent['302']['img']))
print('Формирование странички с результатом. {}\index.html'.format(path))
f=open(path+'\\'+'index.html','w',encoding='utf-8')
f.write(str(html_page))
f.close()
html_path = os.path.abspath(path +'\index.html')
sys.stdout = os.devnull
sys.stderr = os.devnull
os.system("start {}".format(html_path))
