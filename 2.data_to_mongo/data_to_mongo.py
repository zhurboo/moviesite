#读入links.csv，为匹配做准备
import os,json
links = dict()
for line in open('ml-20m/links.csv'):
    links[line.split(",")[1]] = line.split(",")[0]
#连接数据库并测试
import pymongo
myclient = pymongo.MongoClient('cloud/cloud3:8018,cloud4:8018,cloud5:8018')
print (myclient)
mydb = myclient['django']
print(mydb.list_collection_names())

movie_mongo_id = {}

#为多元组创建set
genres = set()
directors = set()
writers = set()
stars = set()
languages = set()

#读取文件并写入movie_movie
movCol = mydb["movie_movie"]
files = os.listdir('ml-20m/movie_info')
insert_datas = []
for file in files:
    if file[0] == '.':
        continue
    with open(os.path.join(os.getcwd(), 'ml-20m/movie_info', file, file+'_new.txt'), 'r') as loadedTXT:
        #movie表的处理
        loadedContent = json.load(loadedTXT)
        newItem = {'id':int(links[file]), 'IMDB_id':file, 'name':loadedContent['name'], 'year':loadedContent['year'], 
                       'duration':loadedContent['duration'], 'summary':loadedContent['summary'], 'rating':loadedContent['rating']}
        insert_datas.append(newItem)
        movie_mongo_id[file] = int(links[file])

        #多元组set的处理
        genres.update(loadedContent.get('genres',['None']))
        genres.update(loadedContent.get('genres',['None']))
        directors.update(loadedContent.get('Directors',['None']))
        directors.update(loadedContent.get('Director',['None']))
        writers.update(loadedContent.get('Writers',['None']))
        writers.update(loadedContent.get('Writer',['None']))
        stars.update(loadedContent.get('Stars',['None']))
        stars.update(loadedContent.get('Star',['None']))
        languages.update(loadedContent.get('languages',['None']))
        languages.update(loadedContent.get('language',['None'])) 

#追加的new电影
count = 131262
files = os.listdir('ml-20m/movie_info_new')
insert_datas_new = []
for file in files:
    if file[0] == '.':
        continue
    count += 1
    with open(os.path.join(os.getcwd(), 'ml-20m/movie_info_new', file, file+'_new.txt'), 'r') as loadedTXT:
        #movie表的处理
        loadedContent = json.load(loadedTXT)
        newItem = {'id':count, 'IMDB_id':file, 'name':loadedContent['name'], 'year':loadedContent['year'], 
                       'duration':loadedContent['duration'], 'summary':loadedContent['summary'], 'rating':loadedContent['rating']}
        insert_datas_new.append(newItem)
        movie_mongo_id[file] = count

        #多元组set的处理
        genres.update(loadedContent.get('genres',['None']))
        genres.update(loadedContent.get('genres',['None']))
        directors.update(loadedContent.get('Directors',['None']))
        directors.update(loadedContent.get('Director',['None']))
        writers.update(loadedContent.get('Writers',['None']))
        writers.update(loadedContent.get('Writer',['None']))
        stars.update(loadedContent.get('Stars',['None']))
        stars.update(loadedContent.get('Star',['None']))
        languages.update(loadedContent.get('languages',['None']))
        languages.update(loadedContent.get('language',['None'])) 

movCol.insert_many(insert_datas)
movCol.insert_many(insert_datas_new)
#终止符与计数
print ('#')
print(count)


gen_mongo_id = {}
dir_mongo_id = {}
wri_mongo_id = {}
sta_mongo_id = {}
lan_mongo_id = {}

genCol = mydb["movie_genre"]
dirCol = mydb["movie_director"]
wriCol = mydb["movie_writer"]
staCol = mydb["movie_actor"]
lanCol = mydb["movie_language"]

#处理各多元组表
count = 1
insert_datas_g = []
for item in genres:
    insert_datas_g.append({'id':count, "name":item.strip()})
    gen_mongo_id[item] = count
    count += 1
print(count)

count = 1
insert_datas_d = []
for item in directors:
    insert_datas_d.append({'id':count, "name":item.strip()})
    dir_mongo_id[item] = count
    count += 1
print(count)

count = 1
insert_datas_w = []
for item in writers:
    insert_datas_w.append({'id':count, "name":item.strip()})
    wri_mongo_id[item] = count
    count += 1
print(count)

count = 1
insert_datas_s = []
for item in stars:
    insert_datas_s.append({'id':count, "name":item.strip()})
    sta_mongo_id[item] = count
    count += 1
print(count)

count = 1
insert_datas_l = []
for item in languages:
    insert_datas_l.append({'id':count, "name":item.strip()})
    lan_mongo_id[item] = count
    count += 1
print(count)

genCol.insert_many(insert_datas_g)
dirCol.insert_many(insert_datas_d) 
wriCol.insert_many(insert_datas_w) 
staCol.insert_many(insert_datas_s) 
lanCol.insert_many(insert_datas_l) 
print('#')



genX = mydb["movie_movie_genres"]
dirX = mydb["movie_movie_directors"]
wriX = mydb["movie_movie_writers"]
staX = mydb["movie_movie_actors"]
lanX = mydb["movie_movie_language"]
gCnt = 0
dCnt = 0
wCnt = 0
sCnt = 0
lCnt = 0
#新电影关联表
files = os.listdir('ml-20m/movie_info_new')
insert_gen_datas = []
insert_dir_datas = []
insert_wri_datas = []
insert_sta_datas = []
insert_lan_datas = []
for file in files:
    if file[0] == '.':
        continue
    with open(os.path.join(os.getcwd(), 'ml-20m/movie_info_new', file, file+'_new.txt'), 'r') as _loadedTXT:
        #对每一个movie表项的处理
        _loadedContent = json.load(_loadedTXT)
        genCom = set()
        dirCom = set()
        wriCom = set()
        staCom = set()
        lanCom = set()
        genCom.update(_loadedContent.get('genres',['None']))
        if('Directors' in _loadedContent):  
            dirCom.update(_loadedContent.get('Directors',['None']))
        else:
            dirCom.update(_loadedContent.get('Director',['None']))
        if('Writers' in _loadedContent):
            wriCom.update(_loadedContent.get('Writers',['None']))
        else:
            wriCom.update(_loadedContent.get('Writer',['None']))
        if('Stars' in _loadedContent):
            staCom.update(_loadedContent.get('Stars',['None']))
        else:
            staCom.update(_loadedContent.get('Star',['None']))
        if('languages' in _loadedContent):
            lanCom.update(_loadedContent.get('languages',['None']))
        else:
            lanCom.update(_loadedContent.get('language',['None'])) 
        #构建表项
    y = movie_mongo_id[file]
    for i in genCom:
        gCnt += 1
        x = gen_mongo_id[i]
        insert_gen_datas.append({'id':gCnt, 'movie_id':y, 'genre_id':x})
    for i in dirCom:
        dCnt += 1
        x = dir_mongo_id[i]
        insert_dir_datas.append({'id':dCnt, 'movie_id':y, 'director_id':x})
    for i in wriCom:
        wCnt += 1
        x = wri_mongo_id[i]
        insert_wri_datas.append({'id':wCnt, 'movie_id':y, 'writer_id':x})
    for i in staCom:
        sCnt += 1
        x = sta_mongo_id[i]
        sta_mongo_id[i]
        insert_sta_datas.append({'id':sCnt, 'movie_id':y, 'actor_id':x})
    for i in lanCom:
        lCnt += 1
        x = lan_mongo_id[i]
        insert_lan_datas.append({'id':lCnt, 'movie_id':y, 'language_id':x})
    
genX.insert_many(insert_gen_datas)
dirX.insert_many(insert_dir_datas)
wriX.insert_many(insert_wri_datas)
staX.insert_many(insert_sta_datas)
lanX.insert_many(insert_lan_datas)
print ('#')


#原电影关联表
files = os.listdir('ml-20m/movie_info')
insert_gen_datas = []
insert_dir_datas = []
insert_wri_datas = []
insert_sta_datas = []
insert_lan_datas = []
for file in files:
    if file[0] == '.':
        continue
    with open(os.path.join(os.getcwd(), 'ml-20m/movie_info', file, file+'_new.txt'), 'r') as _loadedTXT:
        #对每一个movie表项的处理
        _loadedContent = json.load(_loadedTXT)
        genCom = set()
        dirCom = set()
        wriCom = set()
        staCom = set()
        lanCom = set()
        genCom.update(_loadedContent.get('genres',['None']))
        if('Directors' in _loadedContent):  
            dirCom.update(_loadedContent.get('Directors',['None']))
        else:
            dirCom.update(_loadedContent.get('Director',['None']))
        if('Writers' in _loadedContent):
            wriCom.update(_loadedContent.get('Writers',['None']))
        else:
            wriCom.update(_loadedContent.get('Writer',['None']))
        if('Stars' in _loadedContent):
            staCom.update(_loadedContent.get('Stars',['None']))
        else:
            staCom.update(_loadedContent.get('Star',['None']))
        if('languages' in _loadedContent):
            lanCom.update(_loadedContent.get('languages',['None']))
        else:
            lanCom.update(_loadedContent.get('language',['None'])) 

        #构建表项
    y = movie_mongo_id[file]
    for i in genCom:
        gCnt += 1
        x = gen_mongo_id[i]
        insert_gen_datas.append({'id':gCnt, 'movie_id':y, 'genre_id':x})
    for i in dirCom:
        dCnt += 1
        x = dir_mongo_id[i]
        insert_dir_datas.append({'id':dCnt, 'movie_id':y, 'director_id':x})
    for i in wriCom:
        wCnt += 1
        x = wri_mongo_id[i]
        insert_wri_datas.append({'id':wCnt, 'movie_id':y, 'writer_id':x})
    for i in staCom:
        sCnt += 1
        x = sta_mongo_id[i]
        insert_sta_datas.append({'id':sCnt, 'movie_id':y, 'actor_id':x})
    for i in lanCom:
        lCnt += 1
        x = lan_mongo_id[i]
        insert_lan_datas.append({'id':lCnt, 'movie_id':y, 'language_id':x})
    print(lanCom)
genX.insert_many(insert_gen_datas)
dirX.insert_many(insert_dir_datas)
wriX.insert_many(insert_wri_datas)
staX.insert_many(insert_sta_datas)
lanX.insert_many(insert_lan_datas)
print ('#')

