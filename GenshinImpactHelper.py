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

if not os.path.exists(file_path) and not os.path.exists(setting_path): #output_log.txt и settings.ini не найдены
    print('Файлы данных пользователя не найдены.')
    input("Press Enter to continue...")
if not os.path.exists(file_path) and os.path.exists(setting_path): #output_log.txt не найден
    print('Используются ранее сохраненные данные. Возможны расхождения значений.')
    config.read(setting_path)
    region = config.get('Settings','server')
    lang = config.get('Settings','lang')
    authkey_ver = config.get('Settings','authentication_ley_version')
    authkey = config.get('Settings','authentication_key')
    gacha_id = config.get('Check','last_banner_id')
    init_type = config.get('Check','last_banner_code')
if os.path.exists(file_path) and not os.path.exists(setting_path): #settings.ini не найден
    f = open (file_path,'r', encoding="utf-8")
    for line in f:
        if re.search('OnGetWebViewPageFinish:',line):
            if re.search('/log',line):
                dirty_url = str(line)
    f.close()
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
if os.path.exists(file_path) and os.path.exists(setting_path): #оба файла на месте
    f = open (file_path,'r', encoding="utf-8")
    for line in f:
        if re.search('OnGetWebViewPageFinish:',line):
            if re.search('/log',line):
                dirty_url = str(line)
    f.close()
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

gacha_path = path+'\\gacha\\'
try:
    os.mkdir(gacha_path)
except OSError:
    print ("Создать директорию не удалось")
try:
    os.mkdir(gacha_path+region)
except OSError:
    print ("Создать директорию не удалось")

if not os.path.exists(gacha_path+'gacha_custom_code_list'):
    f = open(gacha_path+'gacha_custom_code_list', 'w', encoding='utf-8')
    f.close()
f = open(gacha_path+'gacha_custom_code_list', 'r', encoding='utf-8')
urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_code_list', path+'\\gacha\\gacha_code_list')
gacha_code_file = open(path+'\\gacha\\gacha_code_list', 'r', encoding="utf-8")
gacha_code=[]
for g in gacha_code_file:
    gacha_code.append(g[:-1])
for g in f:
    gacha_code.append(g[:-1])
gacha_code_file.close()
f.close()
if init_type not in gacha_code:
    gacha_code.append(init_type)
    f = open(gacha_path+'gacha_custom_code_list', 'a', encoding='utf-8')
    f.write(init_type+'\n')
    f.close()

for gacha in ['100','200','301','302']:
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
            path_gacha_log = gacha_path+region+'\\'+mydata['data']['list'][0]['uid']
            try:
                os.mkdir(gacha_path+region+'\\'+mydata['data']['list'][0]['uid'])
            except OSError:
                print ("Создать директорию не удалось")
        page = page + 1
    if path_gacha_log != '':
        f = open(path_gacha_log+'\\'+gacha+'.csv', 'w', encoding="utf-8")
        for i in array:
            f.write(i[0]+','+i[1]+'\n')
        f.close()
try:
    os.mkdir(path+'\\items')
except OSError:
    print ("Создать директорию не удалось")
urllib.request.urlretrieve('https://raw.githubusercontent.com/satan007/genshin-impact-gacha-helper/main/gacha_id_list', path+'\\items\\gacha_id_list')
gacha_id_file = open(path+'\\items\\gacha_id_list', 'r', encoding="utf-8")
gacha_id=[]
for g in gacha_id_file:
    gacha_id.append(g)
gacha_id_file.close()
for k in ['os_euro']:
    try:
        os.mkdir(path+'\\items\\'+k)
    except OSError:
        print ("Создать директорию не удалось")
    for j in ['ru-ru','en-us','fr-fr','de-de','es-es','pt-pt','ja-jp','ko-kr','th-th','vi-vn','id-id','zh-tw','zh-cn']:
        try:
            os.mkdir(path+'\\items\\'+k+'\\'+j)
        except OSError:
            print ("Создать директорию не удалось")

        star_5_old = []
        star_4_old = []
        star_3_old = []
        star_5 = []
        star_4 = []
        star_3 = []
        for line in gacha_id:
            items_request = http.request('GET', 'https://webstatic-sea.mihoyo.com/hk4e/gacha_info/%s/%s/%s.json'%(k,line[:-1],j))
            if items_request.status == 200:
                items = items_request.data.decode("UTF-8")
                items = ast.literal_eval(items)
                for s5 in items['r5_prob_list']:
                    star_5_old.append([s5['item_id'],s5['item_type'],s5['item_name']])
                for s4 in items['r4_prob_list']:
                    star_4_old.append([s4['item_id'],s4['item_type'],s4['item_name']])
                for s3 in items['r3_prob_list']:
                    star_3_old.append([s3['item_id'],s3['item_type'],s3['item_name']])
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

        f = open(path+'\\items\\'+k+'\\'+j+'\\star_5.csv','w', encoding="utf-8")
        for l in star_5:
            f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
        f.close()
        f = open(path+'\\items\\'+k+'\\'+j+'\\star_4.csv','w', encoding="utf-8")
        for l in star_4:
            f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
        f.close()
        f = open(path+'\\items\\'+k+'\\'+j+'\\star_3.csv','w', encoding="utf-8")
        for l in star_3:
            f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
        f.close()

#Шаг №3. Получение сохранненых ранее данных и расчет вероятности
gacha_dict={}
gacha_percent={}
s5_index=[]
s4_index=[]
s3_index=[]

lang='ru-ru' #Это надо будет сделать правильным и адекватным
server_name = region #Надо не забыть удалить и поменять
star_5 = open (path+'\\items\\'+server_name+'\\'+lang+'\\star_5.csv','r', encoding="utf-8")
s5=list(csv.reader(star_5))
star_5.close()
star_4 = open (path+'\\items\\'+server_name+'\\'+lang+'\\star_4.csv','r', encoding="utf-8")
s4=list(csv.reader(star_4))
star_4.close()
star_3 = open (path+'\\items\\'+server_name+'\\'+lang+'\\star_3.csv','r', encoding="utf-8")
s3=list(csv.reader(star_3))
star_3.close()

for i in s5:
    s5_index.append(i[0])
for i in s4:
    s4_index.append(i[0])
for i in s3:
    s3_index.append(i[0])

for gacha in ['100','200','301','302']:
    try:
        f = open(gacha_path+'\\'+server_name+'\\'+user_id+'\\'+gacha+'.csv', 'r', encoding="utf-8")
    except:
        print('Файл не найден')
    gacha_dict[gacha]=list(csv.reader(f))
    print(len(gacha_dict[gacha]))
    for i in range(len(gacha_dict[gacha])):
        if gacha_dict[gacha][i][0] in s3_index:
            index = s3_index.index(gacha_dict[gacha][i][0])
            gacha_dict[gacha][i][0] = s3[index][2]
            gacha_dict[gacha][i].append(s3[index][1])
            gacha_dict[gacha][i].append('3')
        elif gacha_dict[gacha][i][0] in s4_index:
            index = s4_index.index(gacha_dict[gacha][i][0])
            gacha_dict[gacha][i][0] = s4[index][2]
            gacha_dict[gacha][i].append(s4[index][1])
            gacha_dict[gacha][i].append('4')
        elif gacha_dict[gacha][i][0] in s5_index:
            index = s5_index.index(gacha_dict[gacha][i][0])
            gacha_dict[gacha][i][0] = s5[index][2]
            gacha_dict[gacha][i].append(s5[index][1])
            gacha_dict[gacha][i].append('5')
        else:
            gacha_dict[gacha][i].append('-1')
    gacha_dict[gacha].reverse()
    s4_percent = 0,0
    s5_percent = 0,0
    s4_count = 1
    s5_count = 1
    for i in gacha_dict[gacha]:
        s4_count=s4_count+1
        s5_count=s5_count+1
        if i[3]=='4':
            s4_count = 1
        elif i[3]=='5':
            s5_count = 1
    s4_percent=(100*s4_count)/10
    s5_percent=(1-((1-0.006)**s5_count))*100
    if s5_count == 90:
        s5_percent=100,0
    gacha_percent[gacha]={'star_4':s4_percent,'star_5':s5_percent}

f=open(path+'\\percent.txt','w',encoding='utf-8')
f.write(str(gacha_percent))
f.close()
print(gacha_percent)
print('end')