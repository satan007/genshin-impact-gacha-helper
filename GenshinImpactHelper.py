import os
import re
import sys
import urllib.request, urllib.parse
import urllib3
import certifi
import ast
import csv
import configparser
import webbrowser

http = urllib3.PoolManager(ca_certs=certifi.where())
environ_username = os.environ['username']
config = configparser.ConfigParser()

path = os.getcwd()
file_path = r'C:\Users\%s\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt' % (environ_username) 
setting_path = path+'\\settings.ini'

if not os.path.exists(file_path) and not os.path.exists(setting_path): #output_log.txt и settings.ini не найдены
    print('Файлы данных пользователя не найдены.')
    input("Press Enter to continue...")
    sys.exit()
elif not os.path.exists(file_path) and os.path.exists(setting_path): #output_log.txt не найден
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
        print('Используются ранее сохраненные данные. Возможны расхождения значений.')
        config.read(setting_path)
        region = config.get('Settings','server')
        lang = config.get('Settings','lang')
        authkey_ver = config.get('Settings','authentication_key_version')
        authkey = config.get('Settings','authentication_key')
        gacha_id = config.get('Check','last_banner_id')
        init_type = config.get('Check','last_banner_code')


gacha_path = path+'\\gacha'
try:
    os.mkdir(gacha_path)
except OSError:
    if not os.path.exists(gacha_path):
        print ("Создать директорию не удалось")
try:
    os.mkdir(gacha_path+'\\'+region)
except OSError:
    if not os.path.exists(gacha_path+'\\'+region):
        print ("Создать директорию не удалось")

if not os.path.exists(gacha_path+'\\'+'gacha_custom_code_list'):
    f = open(gacha_path+'\\'+'gacha_custom_code_list', 'w', encoding='utf-8')
    f.close()
f = open(gacha_path+'\\'+'gacha_custom_code_list', 'r', encoding='utf-8')
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_code_list', path+'\\gacha\\gacha_code_list')
except:
    print ("Не могу загрузить файл https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_code_list")
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
        mydata = ast.literal_eval(dict_str)
        if mydata['data']['list'] == []:
            while_end = 1
        else:
            for item_list in mydata['data']['list']:
                array.append([item_list['item_id'],item_list['time']])
            user_id = mydata['data']['list'][0]['uid']
            path_gacha_log = gacha_path+'\\'+region+'\\'+user_id
            try:
                os.mkdir(path_gacha_log)
            except OSError:
                if not os.path.exists(path_gacha_log):
                    print ("Создать директорию не удалось")
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
try:
    os.mkdir(items_path)
except OSError:
    if not os.path.exists(items_path):
        print ("Создать директорию не удалось")
if not os.path.exists(items_path+'\\'+'gacha_custom_id_list'):
    f = open(items_path+'\\'+'gacha_custom_id_list', 'w', encoding='utf-8')
    f.close()
f = open(items_path+'\\'+'gacha_custom_id_list', 'r', encoding='utf-8')
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_id_list', path+'\\items\\gacha_id_list')
except:
    print ("Не могу загрузить файл https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_id_list")
gacha_id_array=[]

try:
    gacha_id_file = open(items_path+'\\'+'gacha_id_list', 'r', encoding="utf-8")
    for g in gacha_id_file:
        gacha_id_array.append(g)
    gacha_id_file.close()
except:
    print ("Не могу найти файл %s\gacha_id_list" % items_path)
for g in f:
    gacha_id_array.append(g[:-1])
if gacha_id not in gacha_id_array:
    gacha_id_array.append(gacha_id)
    f = open(items_path+'\\'+'gacha_custom_id_list', 'a', encoding='utf-8')
    f.write(gacha_id+'\n')
    f.close()


try:
    os.mkdir(items_path+'\\'+region)
except OSError:
    if not os.path.exists(items_path+'\\'+region):
        print ("Создать директорию не удалось")

try:
    os.mkdir(items_path+'\\'+region+'\\'+lang)
except OSError:
    if not os.path.exists(items_path+'\\'+region+'\\'+lang):
        print ("Создать директорию не удалось")


star_5 = []
star_4 = []
star_3 = []
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/%s/%s/star_3.csv' % (region, lang), path+'\\items\\%s\\%s\\star_3.csv' % (region, lang))
except:
    print ("Не могу загрузить файл https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/%s/%s/star_3.csv" % (region, lang))
    print ("Создаю пустой файл")
    f = open(path+'\\items\\'+region+'\\'+lang+'\\star_3.csv','w', encoding="utf-8")
    f.close()
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/%s/%s/star_4.csv' % (region, lang), path+'\\items\\%s\\%s\\star_4.csv' % (region, lang))
except:
    print ("Не могу загрузить файл https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/%s/%s/star_4.csv" % (region, lang))
    print ("Создаю пустой файл")
    f = open(path+'\\items\\'+region+'\\'+lang+'\\star_4.csv','w', encoding="utf-8")
    f.close()
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/%s/%s/star_5.csv' % (region, lang), path+'\\items\\%s\\%s\\star_5.csv' % (region, lang))
except:
    print ("Не могу загрузить файл https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/items/%s/%s/star_5.csv" % (region, lang))
    print ("Создаю пустой файл")
    f = open(path+'\\items\\'+region+'\\'+lang+'\\star_5.csv','w', encoding="utf-8")
    f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_5.csv','r', encoding="utf-8")
star_5_old = list(csv.reader(f))
f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_3.csv','r', encoding="utf-8")
star_3_old = list(csv.reader(f))
f.close()
f = open(path+'\\items\\'+region+'\\'+lang+'\\star_4.csv','r', encoding="utf-8")
star_4_old = list(csv.reader(f))
f.close()
gacha_id_array = [line.rstrip() for line in gacha_id_array]
for line in gacha_id_array:
    items_request = http.request('GET', 'https://webstatic-sea.mihoyo.com/hk4e/gacha_info/%s/%s/%s.json'%(region,line,lang))
    if items_request.status == 200:
        items = items_request.data.decode("UTF-8")
        items = ast.literal_eval(items)
        for s5 in items['r5_prob_list']:
            star_5_old.append([str(s5['item_id']),s5['item_type'],s5['item_name']])
        for s4 in items['r4_prob_list']:
            star_4_old.append([str(s4['item_id']),s4['item_type'],s4['item_name']])
        for s3 in items['r3_prob_list']:
            star_3_old.append([str(s3['item_id']),s3['item_type'],s3['item_name']])
    else:
        print('as')
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
    gacha_img=''
    for i in gacha_dict[gacha]:
        s4_count=s4_count+1
        s5_count=s5_count+1
        if i[4]=='4':
            s4_count = 1
            gacha_img=gacha_img+'<img style="width: 20%;" src="items/img/{}.png" />'.format(i[0])
        elif i[4]=='5':
            s5_count = 1
            gacha_img=gacha_img+'<img style="width: 20%;" src="items/img/{}.png" />'.format(i[0])
        elif i[4]=='-1':
            gacha_img=gacha_img+'<img style="width: 20%;" src="items/img/{}.png" />'.format(i[0])
        gacha_translated.write(i[2]+','+i[1]+','+i[3]+','+i[4]+'\n')
    s4_percent=(100*s4_count)/10
    s5_percent=(1-((1-0.006)**s5_count))*100
    if s5_count == 90:
        s5_percent=100,0
    gacha_percent[gacha]={'star_4':s4_percent,'star_5':s5_percent,'star_4_count':s4_count,'star_5_count':s5_count,'img':gacha_img,'count':len(gacha_dict[gacha])}
    gacha_translated.close()

html_page = '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no"><title>Untitled</title><link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css"><link rel="stylesheet" href="assets/css/styles.min.css"></head><body style="background-color: #333333;"><div class="container py-5"><div class="row"><div class="col-lg-12 text-center mx-auto mb-5 text-white"><h1 class="display-4 text-white">Genshin Impact Gacha Helper</h1></div></div><div class="row"><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Молитва новичка({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Стандартная молитва({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div></div><div class="row"><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Молитва события персонажа({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div><div class="col col-xl-6 col-lg-6 mb-4"><div class="bg-white rounded-lg p-5 shadow" style="background-color: #ffffff;"><div class="row"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Молитва события оружия({})</h4></div></div><div class="row"><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="text-center"><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="col"><div class="text-center"><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span><span class="star-img"></span></div><div class="progress mx-auto" data-value="{}"><span class="progress-left"><span class="progress-bar border-primary"></span></span><span class="progress-right"><span class="progress-bar border-primary"></span></span><div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center"><div class="h2 font-weight-bold">{}<sup class="small">%</sup></div></div></div></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h4 font-weight-bold mb-0">{}\\10</h4></div><div class="col"><h4 class="font-weight-bold mb-0">{}\\90</h4></div></div><div class="row text-center mt-4"><div class="col"><h4 class="h6 font-weight-bold text-center mb-4">Последние полученные</h4></div></div><div class="row"><div class="col">{}</div></div></div></div></div><span></span></div><script src="assets/js/jquery.min.js"></script><script src="assets/bootstrap/js/bootstrap.min.js"></script><script src="assets/js/script.min.js"></script></body></html>'.format(str(gacha_percent['100']['count']),str(round(gacha_percent['100']['star_4'])),str(round(gacha_percent['100']['star_4'],3)),str(round(gacha_percent['100']['star_5'])),str(round(gacha_percent['100']['star_5'],3)),str(gacha_percent['100']['star_4_count']),str(gacha_percent['100']['star_5_count']),str(gacha_percent['100']['img']),str(gacha_percent['200']['count']),str(round(gacha_percent['200']['star_4'])),str(round(gacha_percent['200']['star_4'],3)),str(round(gacha_percent['200']['star_5'])),str(round(gacha_percent['200']['star_5'],3)),str(gacha_percent['200']['star_4_count']),str(gacha_percent['200']['star_5_count']),str(gacha_percent['200']['img']),str(gacha_percent['301']['count']),str(round(gacha_percent['301']['star_4'])),str(round(gacha_percent['301']['star_4'],3)),str(round(gacha_percent['301']['star_5'])),str(round(gacha_percent['301']['star_5'],3)),str(gacha_percent['301']['star_4_count']),str(gacha_percent['301']['star_5_count']),str(gacha_percent['301']['img']),str(gacha_percent['302']['count']),str(round(gacha_percent['302']['star_4'])),str(round(gacha_percent['302']['star_4'],3)),str(round(gacha_percent['302']['star_5'])),str(round(gacha_percent['302']['star_5'],3)),str(gacha_percent['302']['star_4_count']),str(gacha_percent['302']['star_5_count']),str(gacha_percent['302']['img']))

f=open(path+'\\index.html','w',encoding='utf-8')
f.write(str(html_page))
f.close()
webbrowser.open (path+'\\index.html', new=2)
#print(gacha_percent)
#print('end')