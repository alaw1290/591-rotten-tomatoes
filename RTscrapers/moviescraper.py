from bs4 import BeautifulSoup
import requests
import time
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
import json

base_url = 'https://www.rottentomatoes.com'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'


def moviescraper(movie_urls):
	'''Using the movie_urls dictionary, retrieves page for each movie and stores 
	these attributes in the json: 
	'title':{
		'all_tom':rating,
		'all_avg': rating,
		'all_count': count,
		'all_fresh': count,
		'all_rot': count,
		'top'
		'top_avg': rating,
		'top_count': count,
		'top_fresh': count,
		'top_rot': count,
		'aud_avg':rating,
		'aud_count':count,
		'num_vids': count,
		'num_pics':count,
		'info_rating':'rating',
		'info_genre':[genreids],
		'info_direct':['directors'],
		'info_write':['writers'],
		'info_release':unixtime,
		'info_box': '$',
		'info_studio': 'studio',
		'cast_list':['actors']
	}

	Tolerance to include movie in dataset: 
		all_count > 10, 
		top_count > 10,
		aud_count > 50


	'''

	headers = {'User-Agent' : user_agent }


	with open('test.json','w') as file:

	    #iterate over each movie
	    for title in movie_urls:
	    	response = requests.get(base_url + movie_urls[title], headers=headers)
	    	html = response.text.encode('utf-8')
	    	soup = BeautifulSoup(html,"lxml")

	    	#collect for each

	    	scores = soup.find('div',{'id':'scorePanel'})

	    	
	    	try:

	    		all_tom = int(scores.find('div',{'id':'all-critics-numbers'}).find('a',{'id': 'tomato_meter_link'}).text.split('%')[0])
	    		print(title + ' ' + str(all_tom))

	    		all_avg = float(scores.find('div',{'id':'all-critics-numbers'}).find('div',{'class': 'superPageFontColor'}).text.split(':')[1].strip().split('/')[0])
	    		print(title + ' ' + str(all_tom))

	    		all_count = float(scores.find('div',{'id':'all-critics-numbers'}).find('div',{'class': 'superPageFontColor'}).text.split(':')[1].strip().split('/')[0])
	    		print(title + ' ' + str(all_tom))

	    	except Exception as e:
	    		continue
	    	


if __name__ == '__main__':
	moviescraper({'Star Treck Beyond':'/m/star_trek_beyond', 'My Dead Boyfriend':'/m/my_dead_boyfriend', 'Swiss Army Man': '/m/swiss_army_man', 'phantom house': '/m/the_royal_opera_house_les_contes_dhoffmann'})



















