import requests, csv, json, time, random, os, re, sys
from multiprocessing import Pool
from bs4 import BeautifulSoup


def imdb_spider(url, review_url, spider_dic, id):
	UA = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11", "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"]
	proxies_list = ['http://27.128.187.22:3128', 'https://120.78.225.5:3128', 'https://61.128.208.94:3128', 'http://222.240.184.126:8086', 'https://59.38.62.109:9797', 'http://59.38.60.32:9797', 'http://119.131.88.136:9797', 'https://119.131.89.133:9797', 'https://125.123.121.36:9000', 'https://58.17.125.215:53281', '://171.80.227.51:8118', 'https://113.247.252.114:9090', 'http://175.17.161.20:8080', 'https://124.237.83.14:53281', 'http://59.44.247.194:9797', 'https://122.136.212.132:53281', 'https://183.174.60.5:8080', 'http://183.185.1.47:9797', 'http://182.61.25.65:3128', 'https://113.109.249.32:808', 'http://1.196.161.203:9999', 'http://163.125.249.77:8118', 'http://119.123.177.155:9000', 'http://114.239.3.187:808', 'http://125.123.141.47:9000', 'https://124.16.81.135:1080', 'http://171.11.33.60:9999', 'https://113.140.1.82:53281', 'https://59.38.63.207:9797', 'https://123.139.56.238:9999', 'https://124.152.32.140:53281', 'http://113.65.8.90:9797', 'https://222.90.110.194:8080', 'https://180.103.218.209:8118', 'http://123.117.34.115:9000', 'http://120.27.27.158:3128', 'https://218.22.7.62:53281', 'https://183.129.207.78:18118', '://103.10.86.203:8080', 'http://110.16.80.106:8080', 'http://163.125.65.213:9797', '://118.31.9.50:8118', 'http://163.125.65.166:9797', 'http://163.125.113.86:8118', 'http://163.125.113.222:8118', 'http://183.129.207.86:11206', 'https://182.88.5.99:9797', 'http://60.169.45.87:8118', '://140.143.48.49:1080', 'http://222.249.238.138:8080', 'http://59.38.62.250:9797', 'http://218.108.175.15:80', 'http://101.231.50.154:8000', 'https://59.38.61.173:9797', 'http://14.115.104.77:808', 'http://116.21.122.94:808', 'http://119.131.88.242:9797', 'http://183.129.207.90:31330', 'http://114.249.118.80:9000', 'http://219.131.242.160:9797', 'http://125.88.190.1:3128', 'http://119.48.179.138:9999', 'http://124.205.155.150:9090', 'https://125.123.137.250:9000', 'http://118.114.188.43:1080', 'https://210.26.49.88:3128', 'https://60.211.218.78:53281', 'https://183.129.207.93:13629', 'https://59.38.62.110:9797', 'http://58.249.55.222:9797', '://106.12.24.167:3128', 'http://180.160.60.39:8118', 'http://171.37.79.169:9797', 'http://119.39.68.198:808', 'https://58.250.23.210:1080', 'http://118.25.17.229:80', 'https://58.20.37.25:8181', 'http://218.64.69.79:8080', 'https://218.60.8.83:3129', 'https://210.26.64.44:3128', 'https://221.229.252.98:8080', 'http://221.204.118.108:9797', 'http://163.125.251.250:8118', 'https://218.2.226.42:80', 'https://222.95.26.60:8118', 'https://218.60.8.99:3129', 'http://121.15.254.156:888', 'https://61.130.181.114:9999', 'https://118.187.58.35:53281', 'http://117.85.11.154:8118', '://180.150.185.191:10820', 'https://112.95.205.224:8888', 'https://183.129.207.80:21776', 'http://182.88.116.205:9797', 'https://119.131.89.172:9797', 'https://59.38.60.75:9797', 'https://120.25.164.127:8118', 'http://211.101.154.105:43598', 'https://114.239.148.103:808', 'http://119.48.172.67:9999']
	try:
		r = requests.get(url, headers={'User-Agent':random.choice(UA)})#, proxies = {'http' : random.choice(proxies_list)})
		soup = BeautifulSoup(r.text, features="lxml")
	except Exception:
		print('web spider fails to get %s' %(url), flush=True)
		sys.stdout.flush()
		return -1

	movie_name = soup.find('div', 'title_wrapper').find('h1').text.strip()
	index = movie_name.find('(')
	movie_name = movie_name[:index].strip()
	spider_dic['name'] = movie_name

	spider_dic['duration'] = soup.find("time", attrs={"datetime": re.compile("PT(\d)+M")}).text.strip()
	spider_dic['rating'] = soup.find('div', 'ratingValue').text.strip()
	spider_dic['brief_summary'] = soup.find_all('div', 'summary_text')[0].text.strip()
	spider_dic['summary'] = soup.find('div', attrs={'class' : 'article', 'id' : 'titleStoryLine'}).find('div', 'inline canwrap').find('span').text.strip()

	genres_string = soup.find('div', attrs={'class' : 'article', 'id' : 'titleStoryLine'}).find_all('div', 'see-more inline canwrap')[-1].text.strip()
	index = genres_string.find(':')
	genres_list_temp = genres_string[index + 1:].split('|')
	genres_list = []
	for genre in genres_list_temp:
		genres_list.append(genre.strip())
	spider_dic['genres'] = genres_list

	summary_items = soup.find_all('div', 'credit_summary_item')
	for item in summary_items:
		key = item.find_all('h4', 'inline')[0].text.strip(':')
		value = []
		values = item.find_all('a')
		for i in range(len(values)):
			name = values[i].text.strip()
			if name.endswith('more credits') or name.startswith('See full cast & crew'):
				continue
			else:
				value.append(name)
		spider_dic[key] = value

	movie_detail = soup.find('div', attrs = {'class' : 'article', 'id' : 'titleDetails'}).find_all('div', 'txt-block')
	detail_dic = {}
	for item in movie_detail:
		keyvalue = item.text.strip().replace('\n', '')
		moreindex = keyvalue.find('See more')
		if moreindex != -1:
			keyvalue = keyvalue[:moreindex]
		else:
			keyvalue = keyvalue
		keyindex = keyvalue.find(':')
		key = keyvalue[:keyindex]
		value = keyvalue[keyindex + 1:]
		detail_dic[key] = value

	if 'Release Date' in detail_dic.keys():
		releaseDate = detail_dic['Release Date']
		index = releaseDate.find('(')
		spider_dic['year'] = releaseDate[index - 5 : index - 1]
	else:
		spider_dic['year'] = 'unknown'

	if 'Language' in detail_dic.keys():
		language_list = detail_dic['Language'].split('|')
		spider_dic['language'] = language_list
	else:
		spider_dic['language'] = []

	if 'Production Co' in detail_dic.keys():
		production_list = detail_dic['Production Co'].strip().split(',')
		spider_dic['production'] = production_list
	else:
		spider_dic['production'] = []

	if 'Cumulative Worldwide Gross' in detail_dic.keys():
		spider_dic['gross'] = detail_dic['Cumulative Worldwide Gross']
	else:
		spider_dic['gross'] = 'unknown'

	try:
		review_r = requests.get(review_url, headers={'User-Agent':random.choice(UA)}, proxies = {'http' : random.choice(proxies_list)})
		review_soup = BeautifulSoup(review_r.text, features="lxml")
	except:
		print('web spider fails to get %s\'s review' %(url), flush=True)
		sys.stdout.flush()
		return -1
	review_raw_list = review_soup.find('div', 'lister-list').find_all('div', 'text show-more__control')
	records_num = min(20, len(review_raw_list))
	review_list = []
	for i in range(records_num):
		review_list.append(review_raw_list[i].text)
	spider_dic['review'] = review_list
	movie_json = json.dumps(spider_dic)
	with open('movie_info_new/'+ id + '/' + id + '.txt', 'wt') as f:
		f.write(movie_json)

	pic_url = soup.find('div', 'poster').find('img').get('src')
	try:
		pic_r = requests.get(pic_url, headers={'User-Agent':random.choice(UA)}, proxies = {'http' : random.choice(proxies_list)})
		with open('movie_info_new/' + id + '/'  +id + '_cover.png', 'wb') as f:
			f.write(pic_r.content)
	except:
		print('web spider fails to get %s\'s cover picture' %(url), flush=True)
		sys.stdout.flush()
		return -1
	return 1


def imdb_spider_process(i):
	spider_dic = {}
	url = 'https://www.imdb.com/title/tt' + i + '/'
	review_url = 'https://www.imdb.com/title/tt' + i + '/reviews'
	os.mkdir('movie_info_new/' + i)
	ans = imdb_spider(url, review_url, spider_dic, i)
	if ans == -1:
		print('movie id %s fails!' %(i), flush=True)
		sys.stdout.flush()
	else:
		print('movie id %s succeeds!' %(i), flush=True)
		sys.stdout.flush()
	time.sleep(random.randint(0, 4))


def new_movie_spider(date, keyList):
	try:
		url = 'https://www.imdb.com/showtimes/location/US/90001/' + date
		r = requests.get(url)
		soup = BeautifulSoup(r.text, features="lxml")
	except:
		print('web spider fails to get new movies!', flush=True)
		sys.stdout.flush()
		return
	new_movies = soup.find_all('div', 'title')
	for movie in new_movies:
		href = movie.find('a').get('href')
		index = href.find('tt')
		movie_id = href[index + 2: -1]
		keyList.append(movie_id)
	return


if __name__ == '__main__':
	keyList = []
	new_movie_spider('2019-11-16', keyList)
	print(keyList)
	p = Pool(10)
	for i in range(len(keyList)):
		p.apply_async(imdb_spider_process, args= (keyList[i], ))
	p.close()
	p.join()
	print('All work finished!')
	work_dir =  os.getcwd() + '/movie_info_new/'
	delCommand = 'rm -rf '
	for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
		if parent != work_dir and len(filenames) < 2:
			delCommand += parent
			delCommand += ' '
	print('Deleting!\n%s' %(delCommand))
	os.system(delCommand)