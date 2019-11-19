import requests, csv, json, time, random, os, re
from bs4 import BeautifulSoup


def imdb_spider(url, review_url, spider_dic, id):
	UA = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11", "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"]
	proxies_list = ['http://49.79.192.40:50129', 'http://182.34.35.110:9999', 'http://183.129.244.16:11161', 'http://121.31.160.133:8123', 'http://171.35.161.196:9999', 'http://117.30.112.19:9999', 'http://49.89.220.249:9999', 'http://117.30.112.140:9999', 'http://94.191.40.157:8118', 'http://182.92.233.137:8118', 'http://113.128.31.27:9999', 'http://183.166.20.172:9999', 'http://123.54.47.220:9999', 'http://175.42.123.201:9999', 'http://115.231.5.230:44524', 'http://163.125.114.80:8118', 'http://121.13.252.60:41564', 'http://182.35.80.48:9999', 'http://183.129.244.16:11232', 'http://180.118.128.199:9000', 'http://211.152.33.24:59523', 'http://125.110.77.131:9000', 'http://117.90.2.92:9000', 'http://223.100.166.3:36945', 'http://113.120.32.110:9999', 'http://49.81.125.153:9000', 'http://120.79.184.148:8118', 'http://119.23.148.193:8118', 'http://125.73.220.18:49128', 'http://121.232.148.138:9000', 'http://125.123.122.52:9999', 'http://61.189.242.243:55484', 'http://120.26.199.103:8118', 'http://117.90.4.17:9000', 'http://1.199.132.107:9999', 'http://60.216.101.46:32868', 'http://123.54.45.48:9999', 'http://125.123.66.53:9999', 'http://125.123.127.188:9999', 'http://180.117.128.145:8118', 'http://125.123.71.178:9999', 'http://125.123.69.163:9999', 'http://117.90.1.173:9000', 'http://183.129.244.16:12154', 'http://122.243.11.31:9000', 'http://219.159.38.200:56210', 'http://123.163.20.226:9999', 'http://117.90.2.26:9000', 'http://125.123.124.5:9999', 'http://1.199.31.183:9999', 'http://119.108.179.78:9000', 'http://123.57.84.116:8118', 'http://112.111.116.3:9000', 'http://132.232.104.190:8118', 'http://163.204.247.192:9999', 'http://125.123.125.176:9999', 'http://125.123.65.133:9999', 'http://58.22.207.58:9000', 'http://113.123.28.62:9999', 'http://27.159.167.158:9999', 'http://171.11.179.77:9999', 'http://1.198.72.148:9999', 'http://117.90.137.63:9000', 'http://27.159.165.172:9999', 'http://219.159.38.197:56210', 'http://49.89.103.228:9999', 'http://114.234.81.166:9000', 'http://171.11.33.20:9999', 'http://117.90.5.109:9000', 'http://121.13.252.62:41564', 'http://27.159.165.252:9999', 'http://113.123.28.159:9999', 'http://125.123.125.177:9999', 'http://115.218.213.243:9000', 'http://136.228.128.164:53052', 'http://117.90.252.153:9000', 'http://114.234.83.117:9000', 'http://59.172.27.6:38380', 'http://1.199.30.47:9999', 'http://39.108.90.252:8000', 'http://180.118.86.145:9000', 'http://1.198.73.226:9999', 'http://218.104.61.246:9000', 'http://113.103.227.31:9999', 'http://219.159.38.208:56210', 'http://180.118.86.224:9000', 'http://117.90.0.233:9000', 'http://59.32.37.128:8010', 'http://121.232.199.76:9000', 'http://219.159.38.208:56210', 'http://117.90.4.28:9000', 'http://60.205.229.126:80', 'http://163.204.246.175:9999', 'http://163.204.241.38:9999', 'http://219.159.38.197:56210', 'http://121.232.148.109:9000', 'http://60.205.229.126:80', 'http://171.11.178.236:9999', 'http://163.204.247.173:9999', 'http://47.93.58.5:8118', 'http://36.250.156.209:9999', 'http://163.204.242.29:9999', 'http://183.129.244.16:12585', 'http://121.232.148.97:9000', 'http://180.118.128.166:9000', 'http://59.32.37.205:3128', 'http://49.81.125.131:9000', 'http://115.218.213.59:9000', 'http://175.44.186.84:9000', 'http://125.110.72.41:9000', 'http://118.181.226.216:58654', 'http://183.129.207.80:12806', 'http://49.86.177.173:9999', 'http://219.159.38.200:56210', 'http://163.204.92.100:9999', 'http://47.94.136.5:8118', 'http://175.44.156.226:9000', 'http://61.164.39.69:53281', 'http://118.180.166.195:8060', 'http://112.111.217.141:9999', 'http://163.204.244.101:9999', 'http://114.235.22.14:9000', 'http://171.11.28.113:9999', 'http://59.172.27.6:38380', 'http://1.193.247.148:9999', 'http://120.83.120.242:9999', 'http://120.194.42.157:38185', 'http://163.204.244.166:9999', 'http://47.93.36.195:8118', 'http://222.223.203.104:8060', 'http://117.95.199.186:9999', 'http://183.129.207.92:11056', 'http://47.104.172.108:8118', 'http://123.169.35.16:9999', 'http://120.236.219.12:8060']
	try:
		r = requests.get(url, headers={'User-Agent':random.choice(UA)}, proxies = {'http' : random.choice(proxies_list)})
		soup = BeautifulSoup(r.text, features="lxml")
	except Exception:
		print('web spider fails to get %s' %(url))
		return -1
	spider_dic['duration'] = soup.find("time", attrs={"datetime": re.compile("PT(\d)+M")}).text.strip()
	spider_dic['rating'] = soup.find('div', 'ratingValue').text.strip()
	spider_dic['brief_summary'] = soup.find_all('div', 'summary_text')[0].text.strip()
	spider_dic['summary'] = soup.find('div', attrs={'class' : 'article', 'id' : 'titleStoryLine'}).find('div', 'inline canwrap').find('span').text.strip()

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
		print('web spider fails to get %s\'s review' %(url))
		return -1
	review_raw_list = review_soup.find('div', 'lister-list').find_all('div', 'text show-more__control')
	records_num = min(20, len(review_raw_list))
	review_list = []
	for i in range(records_num):
		review_list.append(review_raw_list[i].text)
	spider_dic['review'] = review_list

	pic_url = soup.find('div', 'poster').find('img').get('src')
	try:
		pic_r = requests.get(pic_url, headers={'User-Agent':random.choice(UA)}, proxies = {'http' : random.choice(proxies_list)})
		with open('movie_info_single/' + id + '/'  + id + '_cover.png', 'wb') as f:
			f.write(pic_r.content)
	except:
		print('web spider fails to get %s\'s cover picture' %(url))
		return -1
	return 1


def movie_id(mvdic, spider_dic, index):
	spider_dic['name'] = mvdic[index]['name']
	spider_dic['year'] = mvdic[index]['year']
	spider_dic['genres'] = mvdic[index]['genres']
	return spider_dic


def readFile(mvdic):
	with open('movies.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		cnt = 0
		for row in spamreader:
			if cnt == 0:
				cnt += 1
				continue
			startindex = row[1].find('(')
			endindex = row[1].find(')')
			mvdic[row[0]] = {}
			mvdic[row[0]]['name'] = row[1][:startindex].strip()
			mvdic[row[0]]['year'] = row[1][startindex + 1 : endindex]
			mvdic[row[0]]['genres'] = row[2].split('|')
		
	with open('links.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		cnt = 0
		for row in spamreader:
			if cnt == 0:
				cnt += 1
				continue
			mvdic[row[0]]['id'] = row[1]
	return


if __name__ == '__main__':
	mvdic = {}
	readFile(mvdic)
	temp = list(mvdic.keys())
	keyList = []
	for i in range(len(temp)):
		keyList.append(int(temp[i]))
	keyList.sort()
	# for i in range(1, 131263):
	for index in range(11639, len(keyList)):
		i = keyList[index]
		spider_dic = {}
		movie_id(mvdic, spider_dic, str(i))
		print(mvdic[str(i)])
		url = 'https://www.imdb.com/title/tt' + mvdic[str(i)]['id'] + '/'
		review_url = 'https://www.imdb.com/title/tt' + mvdic[str(i)]['id'] + '/reviews'
		os.mkdir('movie_info_single/' + mvdic[str(i)]['id'])
		try:
			ans = imdb_spider(url, review_url, spider_dic, mvdic[str(i)]['id'])
		except:
			print('movie id %s fails!' %(mvdic[str(i)]['id']))
			continue
		if ans == -1:
			print('movie id %s fails!' %(mvdic[str(i)]['id']))
		movie_json = json.dumps(spider_dic)
		with open('movie_info_single/' + mvdic[str(i)]['id'] + '/' + mvdic[str(i)]['id'] + '.txt', 'wt') as f:
			f.write(movie_json)
			time.sleep(random.randint(0, 3))
