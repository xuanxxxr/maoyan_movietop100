import requests
import json
from bs4 import BeautifulSoup


def get_html(url):
	try:
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
		r = requests.get(url, timeout = 30,headers=headers)
		r.raise_for_status()
		r.encoding = 'utf-8'
		return r.text
	except:
		return "error"


def get_content(url):
	comments = []
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	dds = soup.find_all('dd')
	# rank = soup.find_all('i',attrs={'class': 'board-index'})
	# print(soup)
	
	for x in dds:
		comment = {}
		comment['pm'] = x.find('i',attrs={'class': 'board-index'}).text
		comment['name'] = x.find('p',attrs = {'class':'name'}).text
		comment['stars'] = x.find('p',attrs={'class': 'star'}).string.strip()
		comment['show'] = x.find('p',attrs={'class': 'releasetime'}).text
		rank1 = x.find('i',attrs = {'class':'integer'}).text
		rank2 = x.find('i',attrs = {'class':'fraction'}).text
		comment['ranks'] = str(rank1) + str(rank2)
		comments.append(comment)
	# return comments
	print(comments)
	
	for i in comments:
		jsObj = json.dumps(i,ensure_ascii=False,indent=2) 
		fileObject = open('top100.json', 'a', encoding = 'utf-8')  
		fileObject.write(jsObj)  
		fileObject.close()



	

def main(base_url):
	url_list = []
	url_list.append(base_url)
	for i in range(10,100,10):
		url_list.append(base_url + '?offset=' + str(i))

	for url in url_list:
		get_content(url)
	# get_content(base_url)


base_url = 'http://maoyan.com/board/4'

if __name__ == "__main__":
	main(base_url)
