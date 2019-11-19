import requests, csv, json, time, random, os, re
from bs4 import BeautifulSoup


def readFile(mvdic):
	with open('movies.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		cnt = 0
		for row in spamreader:
			if cnt == 0:
				cnt += 1
				continue
			startindex = row[1].rfind('(')
			endindex = row[1].rfind(')')
			mvdic[row[0]] = {}
			mvdic[row[0]]['name'] = row[1][:startindex].strip().strip('\"')
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
	keyList = list(mvdic.keys())
	success = 0
	failure = 0
	for i in range(len(keyList)):
		path = 'movie_info/%s/' %(mvdic[str(keyList[i])]['id'])
		try:
			f = open(path + mvdic[str(keyList[i])]['id'] + '.txt', 'r')
			con = f.read()
			dic = json.loads(con)
			dic['name'] = mvdic[str(keyList[i])]['name']
			dic['year'] = mvdic[str(keyList[i])]['year']
			movie_json = json.dumps(dic)
			with open('movie_info/%s/%s_new.txt' %(mvdic[str(keyList[i])]['id'], mvdic[str(keyList[i])]['id']), 'wt') as g:
				g.write(movie_json)
		except:
			print(mvdic[str(keyList[i])]['id'])
			failure += 1
			continue
		else:
			success +=1
	print('%d has succeeded and %d has failed' %(success, failure))
