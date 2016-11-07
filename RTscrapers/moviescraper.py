from bs4 import BeautifulSoup
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

def moviescraper(movie_urls):
	'''Using the movie_urls dictionary, retrieves page for each movie and stores 
	these attributes in the json: 
	'title':{
		'all_avg': rating,
		'all_count': count,
		'all_fresh': count,
		'all_rot': count,
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
	'''

	#create dict
    movie_info = {}

    #start selenium driver
    #driver = webdriver.Firefox()

    #start selenium headless driver
    driver = webdriver.PhantomJS()
    driver.maximize_window()

    #iterate over each movie
    for title in movie_urls:
    	
    	driver.get(movie_urls[title])

    	#run checks for each attribute


